from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Set up the flask-sqlalchemy extension for "new-style" models
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class HelperMethods:
    def to_dict(self):
        return {"location": "from the Helper Method"}

