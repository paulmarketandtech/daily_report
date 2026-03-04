from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DR_",
        case_sensitive=False,
        extra="ignore",
    )

    postgres_user: str = "dailyreport"
    postgres_password: str = os.getenv("DR_DB_PASSWORD")
    postgres_db: str = "dailyreport"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    log_level: str = "INFO"
    environment: str = "development"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
