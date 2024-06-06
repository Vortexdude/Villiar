from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from Viliar.src.extensions.sqla.db_instance import db
from Viliar.src.extensions.sqla import Model, SurrogatePK
from sqlalchemy.types import Boolean


__all__ = ["UserModel"]


class UserModel(Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID, default=lambda: uuid4(), primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    active = db.Column(Boolean, nullable=True)

    def __init__(self, username=None, email=None, password=None, active=True):
        self.username = username
        self.email = email
        self.password = password
        self.active = active

    def to_json(self):
        return {
            "email": self.email,
            "username": self.username,
            "user_id": self.user_id,
            "is_active": self.active
        }

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        data = cls.query.filter_by(email=email).all()
        return {} if len(data) < 1 else data[0]

    def __str__(self):
        return self.email
