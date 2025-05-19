"""Database setup and utility functions."""

import logging
from contextlib import contextmanager
from sqlalchemy.orm import Session as SQLAlchemySession

from fdc.db.session import Session

logger = logging.getLogger(__name__)

@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> SQLAlchemySession:
    """Get a database session. Used for dependency injection."""
    db = Session()
    try:
        yield db
    finally:
        db.close()
