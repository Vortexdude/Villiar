from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import inspect

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

