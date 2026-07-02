from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from avimind_server.db import get_db
from avimind_server.models import Memory
from avimind_server.consolidation_service import consolidate_memories
from avimind_server.schemas import (
    ContextResponse,
    MemoryCreateRequest,
    MemoryResponse,
    MemoryUpdateRequest,
    SearchResponse,
)
from avimind_server.memory_service import (
    create_memory,
    delete_memory,
    get_memory,
    list_memories,
    search_memories,
    update_memory,
)


app = FastAPI(
    title="AviMind",
    description="Open-source Memory OS for AI agents and LLM applications.",
    version="0.6.0",
)


def to_memory_response(
    memory: Memory,
    similarity_score: float | None = None,
    final_score: float | None = None,
) -> MemoryResponse:
    return MemoryResponse(
        id=memory.id,
        user_id=memory.user_id,
        agent_id=memory.agent_id,
        session_id=memory.session_id,
        memory_type=memory.memory_type,
        content=memory.content,
        source=memory.source,
        created_by=memory.created_by,
        tags=memory.tags,
        importance=memory.importance,
        confidence=memory.confidence,
        status=memory.status,
        access_count=memory.access_count,
        last_accessed_at=memory.last_accessed_at,
        expires_at=memory.expires_at,
        version=memory.version,
        parent_memory_id=memory.parent_memory_id,
        metadata=memory.metadata_json,
        similarity_score=similarity_score,
        final_score=final_score,
        created_at=memory.created_at,
        updated_at=memory.updated_at,
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "AviMind",
        "version": "0.6.0",
        "positioning": "Memory OS for AI Agents",
        "features": [
            "sqlite_persistence",
            "postgresql_backend",
            "alembic_migrations",
            "semantic_search",
            "hybrid_retrieval",
            "memory_scoring",
            "automatic_deduplication",
            "memory_lifecycle",
            "soft_delete",
            "access_tracking",
        ],
    }


@app.post("/memory", response_model=MemoryResponse)
def remember_memory(
    request: MemoryCreateRequest,
    db: Session = Depends(get_db),
):
    memory, is_duplicate = create_memory(db, request)
    response = to_memory_response(memory)
    response.metadata = response.metadata or {}
    response.metadata["duplicate_detected"] = is_duplicate
    return response


@app.get("/memory", response_model=list[MemoryResponse])
def list_memory_records(
    user_id: str,
    agent_id: str | None = None,
    session_id: str | None = None,
    memory_type: str | None = None,
    status: str | None = Query(default="active"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    memories = list_memories(
        db=db,
        user_id=user_id,
        agent_id=agent_id,
        session_id=session_id,
        memory_type=memory_type,
        status=status,
        limit=limit,
        offset=offset,
    )

    return [to_memory_response(memory) for memory in memories]


@app.get("/memory/{memory_id}", response_model=MemoryResponse)
def get_memory_record(
    memory_id: str,
    db: Session = Depends(get_db),
):
    memory = get_memory(db, memory_id)

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    return to_memory_response(memory)


@app.patch("/memory/{memory_id}", response_model=MemoryResponse)
def update_memory_record(
    memory_id: str,
    request: MemoryUpdateRequest,
    db: Session = Depends(get_db),
):
    memory = update_memory(db, memory_id, request)

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    return to_memory_response(memory)


@app.get("/memory/search", response_model=SearchResponse)
def search_memory(
    user_id: str,
    query: str,
    agent_id: str | None = None,
    session_id: str | None = None,
    memory_type: str | None = None,
    limit: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    results = search_memories(
        db=db,
        user_id=user_id,
        query=query,
        agent_id=agent_id,
        session_id=session_id,
        memory_type=memory_type,
        limit=limit,
    )

    return SearchResponse(
        results=[
            to_memory_response(
                item["memory"],
                similarity_score=item["similarity_score"],
                final_score=item["final_score"],
            )
            for item in results
        ]
    )


@app.get("/memory/context", response_model=ContextResponse)
def memory_context(
    user_id: str,
    query: str,
    agent_id: str | None = None,
    session_id: str | None = None,
    memory_type: str | None = None,
    limit: int = Query(default=5, ge=1, le=20),
    min_score: float = Query(default=0.65, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
):
    results = search_memories(
        db=db,
        user_id=user_id,
        query=query,
        agent_id=agent_id,
        session_id=session_id,
        memory_type=memory_type,
        limit=limit,
    )

    context = [
        item["memory"].content
        for item in results
        if item["final_score"] >= min_score
    ]

    return ContextResponse(context=context)


@app.delete("/memory/{memory_id}")
def remove_memory(
    memory_id: str,
    db: Session = Depends(get_db),
):
    deleted = delete_memory(db, memory_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")

    return {
        "status": "deleted",
        "memory_id": memory_id,
        "message": "Memory soft deleted successfully.",
    }

@app.post("/memory/consolidate")
def consolidate(
    user_id: str,
    agent_id: str | None = None,
    session_id: str | None = None,
    memory_type: str | None = None,
    min_similarity: float = Query(default=0.85, ge=0.0, le=1.0),
    limit: int = Query(default=100, ge=2, le=500),
    dry_run: bool = True,
    db: Session = Depends(get_db),
):
    return consolidate_memories(
        db=db,
        user_id=user_id,
        agent_id=agent_id,
        session_id=session_id,
        memory_type=memory_type,
        min_similarity=min_similarity,
        limit=limit,
        dry_run=dry_run,
    )