"""Database engine and session handling.

One engine (with a connection pool) is created for the whole process, instead
of a new engine + connection pool on every request.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # drop dead connections instead of crashing
    pool_recycle=1800,    # MySQL closes idle connections; recycle before that
    pool_size=5,
    max_overflow=10,
)

_SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(_SessionFactory)


def get_engine():
    return engine


def get_session():
    """Return the session bound to the current thread/request."""
    return Session()


def remove_session(exception=None):
    """Release the session. Register with `app.teardown_appcontext`."""
    Session.remove()
