import contextlib

import logfire
from decouple import config
from sqlalchemy.inspection import inspect
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = config("DB_CONNECTION")
engine = create_engine(DATABASE_URL)


def is_database_initialized():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    # Get all table names that should exist based on your models
    expected_tables = set()
    for table in SQLModel.metadata.tables.values():
        expected_tables.add(table.name)

    # Check if all expected tables exist
    return expected_tables.issubset(set(existing_tables))

def create_db_and_tables():
    with logfire.span("Creating database and tables"):
        if not is_database_initialized():
            SQLModel.metadata.create_all(engine)
            logfire.info("Database and tables created")
        else:
            logfire.info("Database and tables already exist")

@contextlib.contextmanager
def db_session():
    with contextlib.ExitStack() as stack:
        session = stack.enter_context(Session(engine))
        stack.enter_context(logfire.span("DB Session"))
        try:
            yield session
            session.commit()
        except (SQLModel.SQLModelError, ValueError) as e:
            session.rollback()
            logfire.exception(e)
            raise
        finally:
            session.close()
