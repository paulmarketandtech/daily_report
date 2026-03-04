from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from dailyreport.core.db.base import Base


class Thesis(Base):
    """User investment theses. Thesis is king — always displayed first."""

    __tablename__ = "theses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    linked_tickers: Mapped[list] = mapped_column(
        ARRAY(String(10)), nullable=False, server_default="{}"
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    trigger_description: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[list]] = mapped_column(JSONB, server_default="[]")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (Index("idx_thesis_status", "status"),)
