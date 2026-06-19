from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MemoryCreateRequest(BaseModel):
    user_id: str = Field(..., examples=["demo-user"])
    agent_id: Optional[str] = Field(default=None, examples=["demo-agent"])
    session_id: Optional[str] = Field(default=None, examples=["chat-001"])

    memory_type: str = Field(default="general", examples=["profile_memory"])
    content: str = Field(..., examples=["User prefers AWS Singapore region."])

    source: str = Field(default="manual", examples=["chat"])
    created_by: str = Field(default="human", examples=["human"])

    tags: Optional[List[str]] = Field(default=None, examples=[["aws", "singapore"]])
    importance: float = Field(default=0.5, ge=0.0, le=1.0)

    metadata: Optional[Dict[str, Any]] = None


class MemoryResponse(BaseModel):
    id: str
    user_id: str
    agent_id: Optional[str]
    session_id: Optional[str]

    memory_type: str
    content: str

    source: str
    created_by: str

    tags: Optional[List[str]]
    importance: float

    metadata: Optional[Dict[str, Any]]
    similarity_score: Optional[float] = None
    final_score: Optional[float] = None

    created_at: Optional[datetime] = None


class SearchResponse(BaseModel):
    results: List[MemoryResponse]


class ContextResponse(BaseModel):
    context: List[str]