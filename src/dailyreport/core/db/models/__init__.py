"""Import all models so they register on Base.metadata."""

from dailyreport.core.db.models.company import (  # noqa: F401
    Company,
    CompanyRelationship,
    Sector,
)
from dailyreport.core.db.models.document import (  # noqa: F401
    Document,
    DocumentSection,
)
from dailyreport.core.db.models.knowledge import (  # noqa: F401
    DerivedMetric,
    Mention,
    RawFact,
    RiskFactor,
    Sentiment,
    Summary,
)
from dailyreport.core.db.models.meta import ProcessingLog  # noqa: F401
from dailyreport.core.db.models.thesis import Thesis  # noqa: F401
