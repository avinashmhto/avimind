import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Index, JSON, String, Text

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
    )