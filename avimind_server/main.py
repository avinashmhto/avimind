from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from avimind_server.db import Base, engine, get_db
from avimind_server.models import Memory
from avimind_server.schemas import (
    ContextResponse,
    MemoryCreateRequest,
    MemoryResponse,
    SearchResponse,
)
from avimind_server.memory_service import (
    create_memory,
    delete_memory,
    search_memories,
)

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AviMind",
    description="Open-source persistent memory layer for AI agents and LLM applications.",
    version="0.2.0",
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
        metadata=memory.metadata_json,
        similarity_score=similarity_score,
        final_score=final_score,
        created_at=memory.created_at,
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "AviMind",
        "version": "0.2.0",
        "features": [
            "sqlite_persistence",
            "semantic_search",
            "memory_scoring",
            "automatic_deduplication",
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
    }