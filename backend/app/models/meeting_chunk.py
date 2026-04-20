import os

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

_EMBED_DIM = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))


class MeetingChunk(Base):
    __tablename__ = "meeting_chunks"
    __table_args__ = (
        UniqueConstraint("meeting_id", "chunk_index", name="uq_meeting_chunk_meeting_index"),
        {"schema": "public"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("public.meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(_EMBED_DIM), nullable=False)
