import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError


Base = declarative_base()
session_factory = sessionmaker()
DBSession = scoped_session(session_factory)


def init_db():
    engine = create_engine(os.getenv("DATABASE_URL"))

    import backend.model
    try:
        session_factory.configure(bind=engine)
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        raise SystemExit("OPERATIONAL ERROR: Database cannot be reached on startup.")
