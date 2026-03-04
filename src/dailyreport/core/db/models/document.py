from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dailyreport.core.db.base import Base

if TYPE_CHECKING:
    from dailyreport.core.db.models.company import Company
    from dailyreport.core.db.models.meta import ProcessingLog


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    document_type: Mapped[str] = mapped_column(String(30), nullable=False)
    company_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    publish_date: Mapped[Optional[datetime]] = mapped_column(Date)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    file_path: Mapped[Optional[str]] = mapped_column(String(500))
    file_uri: Mapped[Optional[str]] = mapped_column(String(500))
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), unique=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="queued")
    processing_tier: Mapped[str] = mapped_column(String(20), default="watchlist")
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="documents")
    sections: Mapped[list["DocumentSection"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )
    processing_logs: Mapped[list["ProcessingLog"]] = relationship(
        back_populates="document"
    )

    __table_args__ = (
        Index("idx_doc_company", "company_ticker"),
        Index("idx_doc_type_company", "document_type", "company_ticker"),
        Index("idx_doc_publish_date", "publish_date"),
        Index("idx_doc_status", "status"),
    )


class DocumentSection(Base):
    __tablename__ = "document_sections"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    document_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    section_identifier: Mapped[str] = mapped_column(String(50), nullable=False)
    section_order: Mapped[int] = mapped_column(Integer, default=0)
    raw_text: Mapped[Optional[str]] = mapped_column(Text)
    char_count: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="queued")
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    document: Mapped["Document"] = relationship(back_populates="sections")

    __table_args__ = (
        UniqueConstraint("document_id", "section_identifier", name="uq_doc_section"),
        Index("idx_section_doc", "document_id"),
        Index("idx_section_status", "status"),
    )
