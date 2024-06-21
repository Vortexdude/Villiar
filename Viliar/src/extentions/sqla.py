from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import inspect, create_engine
from typing import Callable
from Viliar.src.config import ConfigParser

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
    pass


db = SQLAlchemy(model_class=Base)


class HelperMethods:

    # dynamically get all the attributes of a model
    def to_dict(self, populate_password=False) -> dict[str, str]:
        """Return a model as a dictionary."""
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        if not populate_password and 'password' in data:
            data.pop('password')
        return data

    def update_with(self, data: dict[str, str]):
        """Update the data with given dict"""
        for k, v in data.items():
            setattr(self, k, v)
        return None
