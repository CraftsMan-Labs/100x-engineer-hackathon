import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

# SQLAlchemy base class for declarative models
Base = declarative_base()

# Create SQLAlchemy engine
def create_database_engine(database_url: str):
    """
    Create a database engine with the given database URL.
    Creates the database if it doesn't exist.
    """
    engine = create_engine(database_url)
    
    if not database_exists(engine.url):
        create_database(engine.url)
    
    return engine

# Create session factory
def create_session_factory(engine):
    """
    Create a session factory for database interactions.
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database connection and session management
def get_db():
    """
    Create a database connection and return a session.
    If the database doesn't exist, it will be created.
    """
    from app.config import get_settings
    
    settings = get_settings()
    engine = create_database_engine(settings.DATABASE_URL)
    SessionLocal = create_session_factory(engine)
    
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
