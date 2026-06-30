import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def build_database_url() -> str:
    db_engine = os.getenv("DB_ENGINE", "sqlite").lower()

    if db_engine == "postgres":
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        if not all([db_host, db_name, db_user, db_password]):
            raise ValueError(
                "PostgreSQL config missing. Please set DB_HOST, DB_NAME, DB_USER, and DB_PASSWORD."
            )

        return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    sqlite_db_path = os.getenv("SQLITE_DB_PATH", "./data/avimind.db")
    Path(sqlite_db_path).parent.mkdir(parents=True, exist_ok=True)

    return f"sqlite:///{sqlite_db_path}"


DATABASE_URL = build_database_url()


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()