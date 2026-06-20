import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine():
    """
    Creates and returns a SQLAlchemy Engine.
    Defaults to a local SQLite database for development if DB_URL is not set.
    """
    db_url = os.getenv("DB_URL", "sqlite:///./traffic_system.db")
    
    connect_args = {}
    if db_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        
    return create_engine(db_url, connect_args=connect_args)

def get_session_factory(engine=None):
    """
    Creates and returns a SQLAlchemy sessionmaker factory.
    """
    if engine is None:
        engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """
    Generator that provides a transactional database session.
    Typically used with FastAPI's Depends() for dependency injection.
    """
    factory = get_session_factory()
    session = factory()
    try:
        yield session
    finally:
        session.close()
