from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from Viliar.src.extensions.sqla.db_instance import db
from Viliar.src.extensions.sqla import Model # SurrogatePK
from sqlalchemy.types import Boolean


__all__ = ["UserModel"]


class SurrogatePK(Model):
    __abstract__ = True
    id = db.Column(db.String, default=lambda: str(uuid4()), primary_key=True)


class UserModel(SurrogatePK):
    __tablename__ = 'users'

    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    active = db.Column(Boolean, nullable=True)
    roles = db.relationship("Role", secondary="user_role", backref=db.backref('users', lazy='dynamic'))

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


class Role(SurrogatePK):
    __tablename__ = "roles"

    name = db.Column(db.String(50), nullable=False)
    policies = db.relationship('Policy', backref='role', lazy=True)


class Policy(SurrogatePK):
    __tablename__ = 'policies'

    name = db.Column(db.String(100), nullable=False)
    resource = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.String(50), db.ForeignKey('roles.id'), nullable=True)

# user role association


class UserRole(SurrogatePK):
    __tablename__ = 'user_role'

    user_id = db.Column(db.String, db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.String, db.ForeignKey('roles.id', ondelete='CASCADE'))
