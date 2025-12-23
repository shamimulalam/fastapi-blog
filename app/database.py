from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session  # Import Session from sqlmodel
import os


def get_database_url():
    """Get database URL based on environment"""
    if os.getenv("TESTING"):
        return "sqlite:///./test_database.db"
    else:
        POSTGRES_USER = os.getenv("POSTGRES_USER", "flashcard_user")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "flashcard_password")
        POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
        POSTGRES_DB = os.getenv("POSTGRES_DB", "flashcard_db")
        return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def get_engine():
    """Create engine based on database type"""
    database_url = get_database_url()

    if database_url.startswith("sqlite"):
        return create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            echo=False
        )
    else:
        return create_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
        )


# Create engine
engine = get_engine()


def create_db_and_tables():
    """Create all tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for FastAPI - yields SQLModel Session"""
    with Session(engine) as session:  # Use SQLModel's Session
        yield session
