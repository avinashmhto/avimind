from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session

from avimind_server.embeddings import (
    cosine_similarity,
    embedding_from_json,
    embedding_to_json,
    generate_embedding,
)
from avimind_server.models import Memory
from avimind_server.schemas import MemoryCreateRequest


DUPLICATE_THRESHOLD = 0.92


def create_memory(db: Session, request: MemoryCreateRequest) -> Tuple[Memory, bool]:
    new_embedding = generate_embedding(request.content)

    existing_memories = (
        db.query(Memory)
        .filter(Memory.user_id == request.user_id)
        .limit(100)
        .all()
    )

    for memory in existing_memories:
        existing_embedding = embedding_from_json(memory.embedding_json)
        if not existing_embedding:
            continue

        similarity = cosine_similarity(new_embedding, existing_embedding)

        if similarity >= DUPLICATE_THRESHOLD:
            memory.importance = max(memory.importance or 0.5, request.importance)
            memory.metadata_json = _merge_metadata(memory.metadata_json, request.metadata)
            db.commit()
            db.refresh(memory)
            return memory, True

    memory = Memory(
        user_id=request.user_id,
        agent_id=request.agent_id,
        session_id=request.session_id,
        memory_type=request.memory_type,
        content=request.content,
        source=request.source,
        created_by=request.created_by,
        tags=request.tags,
        importance=request.importance,
        embedding_json=embedding_to_json(new_embedding),
        metadata_json=request.metadata,
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory, False


def search_memories(
    db: Session,
    user_id: str,
    query: str,
    agent_id: Optional[str] = None,
    session_id: Optional[str] = None,
    memory_type: Optional[str] = None,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    query_embedding = generate_embedding(query)

    db_query = db.query(Memory).filter(Memory.user_id == user_id)

    if agent_id:
        db_query = db_query.filter(
            or_(Memory.agent_id == agent_id, Memory.agent_id.is_(None))
        )

    if session_id:
        db_query = db_query.filter(
            or_(Memory.session_id == session_id, Memory.session_id.is_(None))
        )

    if memory_type:
        db_query = db_query.filter(Memory.memory_type == memory_type)

    memories = db_query.order_by(Memory.created_at.desc()).limit(500).all()

    ranked_results = []

    for memory in memories:
        memory_embedding = embedding_from_json(memory.embedding_json)
        if not memory_embedding:
            continue

        similarity_score = cosine_similarity(query_embedding, memory_embedding)
        importance = memory.importance or 0.5

        final_score = (similarity_score * 0.8) + (importance * 0.2)

        ranked_results.append(
            {
                "memory": memory,
                "similarity_score": round(similarity_score, 4),
                "final_score": round(final_score, 4),
            }
        )

    ranked_results.sort(key=lambda item: item["final_score"], reverse=True)

    return ranked_results[:limit]


def get_context(
    db: Session,
    user_id: str,
    query: str,
    agent_id: Optional[str] = None,
    session_id: Optional[str] = None,
    memory_type: Optional[str] = None,
    limit: int = 5,
) -> List[str]:
    results = search_memories(
        db=db,
        user_id=user_id,
        query=query,
        agent_id=agent_id,
        session_id=session_id,
        memory_type=memory_type,
        limit=limit,
    )

    return [item["memory"].content for item in results]


def delete_memory(db: Session, memory_id: str) -> bool:
    memory = db.query(Memory).filter(Memory.id == memory_id).first()

    if not memory:
        return False

    db.delete(memory)
    db.commit()

    return True


def _merge_metadata(
    existing: Optional[Dict[str, Any]],
    incoming: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    if not existing and not incoming:
        return None

    merged = {}

    if existing:
        merged.update(existing)

    if incoming:
        merged.update(incoming)

    return merged