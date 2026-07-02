import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, Float, Integer, DateTime, Index, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from avimind_server.db import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, nullable=False, index=True)
    agent_id = Column(String, nullable=True, index=True)
    session_id = Column(String, nullable=True, index=True)

    memory_type = Column(String, default="general", index=True)
    content = Column(Text, nullable=False)

    source = Column(String, default="manual", index=True)
    created_by = Column(String, default="human", index=True)

    tags = Column(JSON, nullable=True)
    importance = Column(Float, default=0.5)

    # Memory OS lifecycle fields
    status = Column(String, default="active", index=True)
    access_count = Column(Integer, default=0)
    last_accessed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True, index=True)
    version = Column(Integer, default=1)
    confidence = Column(Float, default=1.0)
    parent_memory_id = Column(String, nullable=True, index=True)

    embedding_json = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        Index("idx_memory_user_agent_type", "user_id", "agent_id", "memory_type"),
        Index("idx_memory_user_session", "user_id", "session_id"),
        Index("idx_memory_user_status", "user_id", "status"),
        Index("idx_memory_lifecycle", "status", "expires_at"),
    )

class MemoryRelationship(Base):
    __tablename__ = "memory_relationships"

    id = Column(String(64), primary_key=True, index=True)

    source_memory_id = Column(
        String(255),
        ForeignKey("memories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    target_memory_id = Column(
        String(255),
        ForeignKey("memories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    relationship_type = Column(String(50), nullable=False, index=True)

    confidence = Column(Float, default=1.0)
    weight = Column(Float, default=1.0)

    metadata_json = Column(JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow)

    source_memory = relationship(
        "Memory",
        foreign_keys=[source_memory_id],
        backref="outgoing_relationships",
    )

    target_memory = relationship(
        "Memory",
        foreign_keys=[target_memory_id],
        backref="incoming_relationships",
    )