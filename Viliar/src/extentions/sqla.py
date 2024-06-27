from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import inspect, create_engine
from typing import Callable
from Viliar.src.config import ConfigParser
from sqlalchemy import MetaData, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from datetime import datetime, UTC, date

DATABASE_URL = ConfigParser().database_uri
engine = create_engine(DATABASE_URL)
SessionLocal: Callable = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Set up the flask-sqlalchemy extension for "new-style" models
class Base(DeclarativeBase):
    metadata = MetaData(schema='public')


db = SQLAlchemy(model_class=Base)


class HelperMethods:

    # dynamically get all the attributes of a model
    def to_dict(self, populate_password=False) -> dict[str, str]:
        """Return a model as a dictionary."""
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        keys_to_remove = [key for key in data.keys() if key.startswith("id") or key.endswith("id")]
        for _key in keys_to_remove:
            data.pop(_key)
        if not populate_password and 'password' in data:
            data.pop('password')
        return data

    def update_with(self, data: dict[str, str]):
        """Update the data with given dict"""
        for k, v in data.items():
            setattr(self, k, v)
        return None


class SurrogatePK(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String, default=lambda: str(uuid4()), primary_key=True, nullable=False)


def now_in_utc() -> datetime:
    """Current time in UTC"""
    return datetime.now(tz=UTC)
