from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.dailyreport.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(bind=engine)


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
