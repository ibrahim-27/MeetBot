from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Meeting(Base):
    __tablename__ = "meetings"
    __table_args__ = {"schema": "public"}

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    is_summarised: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_vectorized: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
