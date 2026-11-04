from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10,
)

_SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(_SessionFactory)


def get_engine():
    return engine


def get_session():
    return Session()


def remove_session(exception=None):
    Session.remove()
