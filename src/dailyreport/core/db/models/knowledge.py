from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dailyreport.core.db.base import Base

if TYPE_CHECKING:
    from dailyreport.core.db.models.company import Company


class RawFact(Base):
    """Immutable facts extracted by the LLM. Never modified after creation."""

    __tablename__ = "raw_facts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    company_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    document_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("documents.id"), nullable=False
    )
    section_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("document_sections.id")
    )
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    numeric_value: Mapped[Optional[float]] = mapped_column(Float)
    text_value: Mapped[Optional[str]] = mapped_column(Text)
    unit: Mapped[Optional[str]] = mapped_column(String(20))
    period_type: Mapped[Optional[str]] = mapped_column(String(20))
    period_identifier: Mapped[Optional[str]] = mapped_column(String(20))
    extraction_confidence: Mapped[Optional[float]] = mapped_column(Float)
    context: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="raw_facts")

    __table_args__ = (
        Index("idx_fact_company", "company_ticker"),
        Index("idx_fact_metric", "metric_name"),
        Index("idx_fact_period", "company_ticker", "metric_name", "period_identifier"),
        Index("idx_fact_document", "document_id"),
        CheckConstraint(
            "extraction_confidence IS NULL OR "
            "(extraction_confidence >= 0 AND extraction_confidence <= 1)",
            name="ck_fact_confidence_range",
        ),
    )


class DerivedMetric(Base):
    """Calculated by Python, NOT the LLM. Can be recomputed at any time."""

    __tablename__ = "derived_metrics"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    company_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    calculated_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(20))
    period_identifier: Mapped[Optional[str]] = mapped_column(String(20))
    calculation_method: Mapped[str] = mapped_column(Text, nullable=False)
    source_fact_ids: Mapped[Optional[list]] = mapped_column(ARRAY(BigInteger))
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="derived_metrics")

    __table_args__ = (
        Index("idx_derived_company_metric", "company_ticker", "metric_name"),
        Index(
            "idx_derived_period",
            "company_ticker",
            "metric_name",
            "period_identifier",
        ),
    )


class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    company_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    document_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("documents.id"), nullable=False
    )
    section_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("document_sections.id")
    )
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary_type: Mapped[str] = mapped_column(String(30), nullable=False)
    # 384 dimensions = all-MiniLM-L6-v2. Change if using different model.
    embedding: Mapped[Optional[list]] = mapped_column(Vector(384))
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="summaries")

    __table_args__ = (
        Index("idx_summary_company", "company_ticker"),
        Index("idx_summary_document", "document_id"),
        Index("idx_summary_type", "summary_type"),
    )


class Sentiment(Base):
    __tablename__ = "sentiment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    company_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    source_type: Mapped[str] = mapped_column(String(30), nullable=False)
    assessed_date: Mapped[date] = mapped_column(Date, nullable=False)
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=False)
    narrative_category: Mapped[Optional[str]] = mapped_column(String(30))
    document_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("documents.id")
    )
    reasoning: Mapped[Optional[str]] = mapped_column(Text)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="sentiments")

    __table_args__ = (
        Index("idx_sentiment_company_date", "company_ticker", "assessed_date"),
        Index("idx_sentiment_source", "source_type"),
        Index("idx_sentiment_narrative", "narrative_category"),
        CheckConstraint(
            "sentiment_score >= -1 AND sentiment_score <= 1",
            name="ck_sentiment_score_range",
        ),
    )


class RiskFactor(Base):
    __tablename__ = "risk_factors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    company_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    risk_category: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_new_this_period: Mapped[bool] = mapped_column(Boolean, default=False)
    document_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("documents.id"), nullable=False
    )
    severity: Mapped[Optional[str]] = mapped_column(String(20))
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="risk_factors")

    __table_args__ = (
        Index("idx_risk_company", "company_ticker"),
        Index("idx_risk_category", "risk_category"),
        Index("idx_risk_new", "is_new_this_period"),
    )


class Mention(Base):
    __tablename__ = "mentions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    document_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("documents.id"), nullable=False
    )
    source_company_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    mentioned_ticker: Mapped[str] = mapped_column(String(10), nullable=False)
    context_snippet: Mapped[Optional[str]] = mapped_column(Text)
    mention_type: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("idx_mention_source", "source_company_ticker"),
        Index("idx_mention_mentioned", "mentioned_ticker"),
        Index("idx_mention_document", "document_id"),
    )
