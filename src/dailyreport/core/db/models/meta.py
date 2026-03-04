from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dailyreport.core.db.base import Base

if TYPE_CHECKING:
    from dailyreport.core.db.models.document import Document


class ProcessingLog(Base):
    """Every LLM API call is logged. No exceptions."""

    __tablename__ = "processing_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    document_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("documents.id")
    )
    section_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("document_sections.id")
    )
    prompt_template_id: Mapped[Optional[str]] = mapped_column(String(100))
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tokens_in: Mapped[int] = mapped_column(Integer, nullable=False)
    tokens_out: Mapped[int] = mapped_column(Integer, nullable=False)
    processing_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, default=dict)

    document: Mapped[Optional["Document"]] = relationship(
        back_populates="processing_logs"
    )

    __table_args__ = (
        Index("idx_proclog_timestamp", "timestamp"),
        Index("idx_proclog_document", "document_id"),
        Index("idx_proclog_model", "model_name"),
        Index("idx_proclog_success", "success"),
    )
