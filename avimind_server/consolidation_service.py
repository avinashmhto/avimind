import json
import math
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from avimind_server.models import Memory, MemoryRelationship

load_dotenv()


def _new_id(prefix: str = "mem") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def _parse_embedding(value: Any) -> Optional[List[float]]:
    if not value:
        return None

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            return None

    return None


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def find_consolidation_candidates(
    db: Session,
    user_id: str,
    agent_id: Optional[str] = None,
    session_id: Optional[str] = None,
    memory_type: Optional[str] = None,
    min_similarity: float = 0.85,
    limit: int = 100,
) -> List[List[Memory]]:
    query = db.query(Memory).filter(
        Memory.user_id == user_id,
        Memory.status == "active",
    )

    if agent_id:
        query = query.filter(Memory.agent_id == agent_id)

    if session_id:
        query = query.filter(Memory.session_id == session_id)

    if memory_type:
        query = query.filter(Memory.memory_type == memory_type)

    memories = query.order_by(Memory.created_at.desc()).limit(limit).all()

    groups: List[List[Memory]] = []
    used_ids = set()

    for memory in memories:
        if memory.id in used_ids:
            continue

        emb_a = _parse_embedding(memory.embedding_json)
        if not emb_a:
            continue

        group = [memory]

        for other in memories:
            if other.id == memory.id or other.id in used_ids:
                continue

            emb_b = _parse_embedding(other.embedding_json)
            if not emb_b:
                continue

            similarity = _cosine_similarity(emb_a, emb_b)

            if similarity >= min_similarity:
                group.append(other)

        if len(group) >= 2:
            for item in group:
                used_ids.add(item.id)
            groups.append(group)

    return groups


def _build_deterministic_summary(memories: List[Memory]) -> str:
    contents = [m.content.strip() for m in memories if m.content]

    if not contents:
        return "Consolidated memory created from related memories."

    combined = " ".join(contents)

    if len(combined) <= 500:
        return f"Consolidated insight: {combined}"

    return f"Consolidated insight: {combined[:500]}..."


def _build_llm_summary(memories: List[Memory]) -> str:
    contents = [m.content.strip() for m in memories if m.content]

    if not contents:
        return "Consolidated memory created from related memories."

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("[AviMind] OPENAI_API_KEY not found. Using deterministic summary.")
        return _build_deterministic_summary(memories)

    try:
        from openai import OpenAI

        print("[AviMind] Using OpenAI for memory consolidation.")

        client = OpenAI(api_key=api_key)

        memory_text = "\n".join(f"- {content}" for content in contents)

        prompt = f"""
You are AviMind, a Memory OS for AI agents.

Consolidate these related memories into one accurate long-term memory.

Rules:
- Do not invent facts.
- Preserve the user's intent.
- Remove duplicate meaning.
- Keep it concise.
- Write as one clear memory statement.
- Do not mention "source memories".
- Do not use bullet points.

Memories:
{memory_text}

Consolidated memory:
""".strip()

        response = client.chat.completions.create(
            model=os.getenv("AVIMIND_LLM_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "You consolidate related memories into accurate long-term memory.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=120,
        )

        summary = response.choices[0].message.content

        if not summary or not summary.strip():
            print("[AviMind] Empty LLM summary. Using deterministic summary.")
            return _build_deterministic_summary(memories)

        return summary.strip()

    except Exception as exc:
        print(f"[AviMind] LLM consolidation failed: {exc}")
        print("[AviMind] Falling back to deterministic summary.")
        return _build_deterministic_summary(memories)


def create_consolidated_memory(
    db: Session,
    memories: List[Memory],
    summary: Optional[str] = None,
) -> Memory:
    first = memories[0]
    now = datetime.utcnow()

    consolidated = Memory(
        id=_new_id("mem"),
        user_id=first.user_id,
        agent_id=first.agent_id,
        session_id=first.session_id,
        memory_type="consolidated",
        content=summary or _build_llm_summary(memories),
        source="consolidation_engine",
        created_by="system",
        tags=["consolidated"],
        importance=max(m.importance or 0.5 for m in memories),
        confidence=max(m.confidence or 0.8 for m in memories),
        status="active",
        version=1,
        access_count=0,
        embedding_json=first.embedding_json,
        metadata_json={
            "consolidated_from": [m.id for m in memories],
            "source_count": len(memories),
            "created_by_feature": "memory_consolidation",
            "summary": {
                "provider": "openai",
                "model": os.getenv("AVIMIND_LLM_MODEL", "gpt-4o-mini"),
                "method": "llm",
                "fallback_used": False,
                "generated_at": now.isoformat(),
            },
        },
        created_at=now,
        updated_at=now,
    )

    db.add(consolidated)
    db.flush()

    return consolidated


def create_relationships(
    db: Session,
    consolidated_memory: Memory,
    source_memories: List[Memory],
    confidence: float = 0.9,
) -> List[MemoryRelationship]:
    relationships = []

    for source_memory in source_memories:
        relationship = MemoryRelationship(
            id=_new_id("rel"),
            source_memory_id=consolidated_memory.id,
            target_memory_id=source_memory.id,
            relationship_type="derived_from",
            confidence=confidence,
            weight=1.0,
            metadata_json={"created_by": "memory_consolidation"},
            created_at=datetime.utcnow(),
        )

        db.add(relationship)
        relationships.append(relationship)

    db.flush()
    return relationships


def archive_source_memories(
    db: Session,
    source_memories: List[Memory],
    parent_memory_id: str,
) -> None:
    for memory in source_memories:
        memory.status = "archived"
        memory.parent_memory_id = parent_memory_id
        memory.updated_at = datetime.utcnow()

    db.flush()


def consolidate_memories(
    db: Session,
    user_id: str,
    agent_id: Optional[str] = None,
    session_id: Optional[str] = None,
    memory_type: Optional[str] = None,
    min_similarity: float = 0.85,
    limit: int = 100,
    dry_run: bool = True,
) -> Dict[str, Any]:
    candidate_groups = find_consolidation_candidates(
        db=db,
        user_id=user_id,
        agent_id=agent_id,
        session_id=session_id,
        memory_type=memory_type,
        min_similarity=min_similarity,
        limit=limit,
    )

    result: Dict[str, Any] = {
        "dry_run": dry_run,
        "groups_found": len(candidate_groups),
        "consolidated_count": 0,
        "groups": [],
    }

    for group in candidate_groups:
        summary = _build_llm_summary(group)

        group_result = {
            "source_memory_ids": [m.id for m in group],
            "source_contents": [m.content for m in group],
            "summary": summary,
            "consolidated_memory_id": None,
            "relationship_ids": [],
        }

        if not dry_run:
            consolidated = create_consolidated_memory(
                db=db,
                memories=group,
                summary=summary,
            )

            relationships = create_relationships(
                db=db,
                consolidated_memory=consolidated,
                source_memories=group,
                confidence=min_similarity,
            )

            archive_source_memories(
                db=db,
                source_memories=group,
                parent_memory_id=consolidated.id,
            )

            group_result["consolidated_memory_id"] = consolidated.id
            group_result["relationship_ids"] = [r.id for r in relationships]

            result["consolidated_count"] += 1

        result["groups"].append(group_result)

    if not dry_run:
        db.commit()

    return result