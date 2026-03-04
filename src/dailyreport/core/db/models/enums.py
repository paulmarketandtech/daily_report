import enum


class DocumentType(str, enum.Enum):
    SEC_10K = "10k"
    EARNINGS_CALL = "earnings_call"
    NEWS = "news"
    MANUAL_NOTE = "manual_note"


class ProcessingStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class SectionType(str, enum.Enum):
    ITEM_1 = "item_1"
    ITEM_1A = "item_1a"
    ITEM_7 = "item_7"
    ITEM_7A = "item_7a"
    ITEM_8 = "item_8"
    PREPARED_REMARKS = "prepared_remarks"
    QA = "qa"
    FULL_DOCUMENT = "full_document"


class SummaryType(str, enum.Enum):
    SECTION_LEVEL = "section_level"
    DOCUMENT_LEVEL = "document_level"


class SentimentSource(str, enum.Enum):
    NEWS = "news"
    SOCIAL = "social"
    EARNINGS_CALL = "earnings_call"
    SEC_10K = "10k"
    MANUAL_NOTE = "manual_note"


class NarrativeCategory(str, enum.Enum):
    GROWTH_STORY = "growth_story"
    TURNAROUND = "turnaround"
    OVERVALUED = "overvalued"
    UNDERVALUED = "undervalued"
    REGULATORY_RISK = "regulatory_risk"
    COMPETITIVE_THREAT = "competitive_threat"
    MARKET_LEADER = "market_leader"
    DECLINING = "declining"
    STABLE = "stable"
    NEUTRAL = "neutral"


class RiskCategory(str, enum.Enum):
    REGULATORY = "regulatory"
    MACRO = "macro"
    COMPETITIVE = "competitive"
    SUPPLY_CHAIN = "supply_chain"
    TECHNOLOGY = "technology"
    FINANCIAL = "financial"
    LEGAL = "legal"
    OPERATIONAL = "operational"
    GEOPOLITICAL = "geopolitical"
    ESG = "esg"


class CompanyRelationType(str, enum.Enum):
    SUPPLIER = "supplier"
    CUSTOMER = "customer"
    COMPETITOR = "competitor"
    PARTNER = "partner"


class MentionType(str, enum.Enum):
    COMPETITOR = "competitor"
    PARTNER = "partner"
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    GENERAL = "general"


class ThesisStatus(str, enum.Enum):
    ACTIVE = "active"
    TRIGGERED = "triggered"
    ACTED_ON = "acted_on"
    INVALIDATED = "invalidated"


class PeriodType(str, enum.Enum):
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    TTM = "ttm"


class MetricUnit(str, enum.Enum):
    DOLLARS = "dollars"
    PERCENTAGE = "percentage"
    COUNT = "count"
    RATIO = "ratio"
    BASIS_POINTS = "basis_points"
