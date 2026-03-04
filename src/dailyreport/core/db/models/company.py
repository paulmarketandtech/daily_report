from datetime import datetime
from typing import TYPE_CHECKING, Optional

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
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dailyreport.core.db.base import Base

if TYPE_CHECKING:
    from dailyreport.core.db.models.document import Document
    from dailyreport.core.db.models.knowledge import (
        DerivedMetric,
        RawFact,
        RiskFactor,
        Sentiment,
        Summary,
    )


class Sector(Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    companies: Mapped[list["Company"]] = relationship(back_populates="sector")


class Company(Base):
    __tablename__ = "companies"

    ticker: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sector_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("sectors.id"))
    industry: Mapped[Optional[str]] = mapped_column(String(255))
    market_cap_range: Mapped[Optional[str]] = mapped_column(String(20))
    is_watchlist: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_processed: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    sector: Mapped[Optional["Sector"]] = relationship(back_populates="companies")
    documents: Mapped[list["Document"]] = relationship(back_populates="company")
    raw_facts: Mapped[list["RawFact"]] = relationship(back_populates="company")
    derived_metrics: Mapped[list["DerivedMetric"]] = relationship(
        back_populates="company"
    )
    summaries: Mapped[list["Summary"]] = relationship(back_populates="company")
    sentiments: Mapped[list["Sentiment"]] = relationship(back_populates="company")
    risk_factors: Mapped[list["RiskFactor"]] = relationship(back_populates="company")

    __table_args__ = (
        Index("idx_company_watchlist", "is_watchlist"),
        Index("idx_company_sector", "sector_id"),
    )


class CompanyRelationship(Base):
    __tablename__ = "company_relationships"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    company_a_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    company_b_ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("companies.ticker"), nullable=False
    )
    relationship_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_document_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("documents.id")
    )
    first_seen: Mapped[Optional[datetime]] = mapped_column(
        Date, server_default=func.current_date()
    )
    last_seen: Mapped[Optional[datetime]] = mapped_column(
        Date, server_default=func.current_date()
    )
    confidence: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "company_a_ticker",
            "company_b_ticker",
            "relationship_type",
            name="uq_company_relationship",
        ),
        CheckConstraint(
            "company_a_ticker != company_b_ticker",
            name="ck_no_self_relationship",
        ),
        Index("idx_comprel_a", "company_a_ticker"),
        Index("idx_comprel_b", "company_b_ticker"),
    )
