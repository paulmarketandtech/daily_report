from datetime import datetime, timezone
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from dailyreport.core.config import settings
from dailyreport.core.db.models import (
    Company,
    Document,
    DocumentType,
    ProcessingStatus,
    Thesis,
    ThesisStatus,
    Sentiment,
    SentimentSource,
)

engine = create_engine(settings.database_url)


def test():
    with Session(engine) as session:
        print("=== Companies ===")
        companies = (
            session.execute(select(Company).where(Company.is_watchlist == True))
            .scalars()
            .all()
        )
        for c in companies:
            print(f"  {c}")

        nvda = session.execute(
            select(Company).where(Company.ticker == "NVDA")
        ).scalar_one()

        print("\n=== Registering test document ===")
        doc = Document(
            company_id=nvda.id,
            doc_type=DocumentType.TEN_Q,
            file_path="0_1.md",
            title="NVIDIA 10-K FY2024",
            period_year=2024,
            status=ProcessingStatus.QUEUED,
        )
        session.add(doc)
        session.flush()
        print(f"  {doc}")

        print("\n=== Creating test thesis ===")
        thesis = Thesis(
            title="NVDA data center dominance",
            body="NVIDIA's data center revenue is growing 200%+ YoY. "
            "Watch for enterprise AI adoption as the next catalyst. "
            "Risk: AMD MI300 competition.",
            linked_tickers=["NVDA", "AMD", "AVGO"],
            status=ThesisStatus.ACTIVE,
            implied_trigger="Enterprise AI spending accelerates in F500",
            notes=[
                {
                    "date": "2024-01-15",
                    "note": "Q4 earnings confirmed data center strength",
                }
            ],
        )
        session.add(thesis)
        session.flush()
        print(f"  {thesis}")

        print("\n=== Theses linked to NVDA ===")
        nvda_theses = (
            session.execute(
                select(Thesis)
                .where(Thesis.linked_tickers.any("NVDA"))
                .where(Thesis.status == ThesisStatus.ACTIVE)
            )
            .scalars()
            .all()
        )
        for t in nvda_theses:
            print(f"  {t}")
            print(f"    Trigger: {t.implied_trigger}")
            print(f"    Notes: {len(t.notes)} entries")

        print("\n=== Adding sentiment ===")
        sent = Sentiment(
            company_id=nvda.id,
            source=SentimentSource.NEWS,
            score=0.8,
            narrative_category="growth_story",
            summary="Reuters reports NVIDIA Q4 data center revenue "
            "exceeded expectations by 15%",
            assessed_at=datetime.now(timezone.utc),
        )
        session.add(sent)
        session.flush()
        print(f"  {sent}")

        session.rollback()
        print("\n=== All tests passed. Rolled back test data. ===")


if __name__ == "__main__":
    test()
