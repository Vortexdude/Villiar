from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from Viliar.src.extensions.sqla import db


__all__ = ["UserModel"]


class Base(db.Model):
    __abstract__ = True
    __tablename__ = "Users"

    user_id = db.Column(UUID, primary_key=True, default=lambda: str(uuid4()))
    email = db.Column(db.String)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,
                           default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())


class UserModel(Base):
    __tablename__ = 'users'

    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    encrypted_password = db.Column(db.String, nullable=False)

    # def set_password(self, password):
    #     self.encrypted_password = bc.generate_password_hash(password)
    #
    # def verify_password(self, password):
    #     return bc.check_password_hash(self.encrypted_password, password)


