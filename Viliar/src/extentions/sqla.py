from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import inspect, create_engine

DATABASE_URL = "postgresql://viliar:botleneck@127.0.0.1/viliar"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
    def to_dict(self) -> dict[str, str]:
        """Return a model as a dictionary."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def update_with(self, data: dict[str, str]):
        """Update the data with given dict"""
        for k, v in data.items():
            setattr(self, k, v)
        return None
