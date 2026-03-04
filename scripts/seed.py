from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dailyreport.core.config import settings
from dailyreport.core.db.models.company import Sector, Company

engine = create_engine(settings.database_url)

SECTORS = [
    "Technology",
    "Healthcare",
    "Financials",
    "Consumer Discretionary",
    "Consumer Staples",
    "Industrials",
    "Energy",
    "Materials",
    "Real Estate",
    "Utilities",
    "Communication Services",
]

TEST_COMPANIES = [
    ("NVDA", "NVIDIA Corporation", "Technology"),
    ("AVGO", "Broadcom Inc.", "Technology"),
    ("IREN", "Iris Energy Limited", "Technology"),
    ("ADI", "Analog Devices Inc.", "Technology"),
]


def seed():
    with Session(engine) as session:
        for name in SECTORS:
            existing = session.query(Sector).filter_by(name=name).first()
            if not existing:
                session.add(Sector(name=name))
                print(f"  Added sector: {name}")

        session.flush()

        for ticker, name, sector_name in TEST_COMPANIES:
            existing = session.query(Company).filter_by(ticker=ticker).first()
            if not existing:
                sector = session.query(Sector).filter_by(name=sector_name).first()
                session.add(
                    Company(
                        ticker=ticker,
                        name=name,
                        sector_id=sector.id if sector else None,
                        is_watchlist=True,
                    )
                )
                print(f"  Added company: {ticker} - {name}")

        session.commit()
        print("\nDone. Seed data inserted.")

        companies = session.query(Company).all()
        print(f"\nCompanies in database: {len(companies)}")
        for c in companies:
            print(f"  {c}")


if __name__ == "__main__":
    seed()
