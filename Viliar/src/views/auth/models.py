from Viliar.src.extentions.sqla import HelperMethods, Base, get_db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Table, Column, ForeignKey, DateTime
from uuid import uuid4
from datetime import datetime, UTC
from typing import List, Optional, Any
from sqlalchemy.exc import PendingRollbackError
db = next(get_db())


def now_in_utc() -> datetime:
    """Current time in UTC"""
    return datetime.now(tz=UTC)


class SurrogatePK(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String, default=lambda: str(uuid4()), primary_key=True, nullable=False)


class UserModel(SurrogatePK, HelperMethods):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    fullname: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_datatime: Mapped[datetime] = mapped_column(
        DateTime, default=now_in_utc, onupdate=now_in_utc,nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=now_in_utc, onupdate=now_in_utc,nullable=True
    )  # New field

    def __init__(self, username, email, password, active=True, fullname=None, **kw: Any):
        super().__init__(**kw)
        self.fullname = fullname if fullname else username
        self.username = username
        self.email = email
        self.password = password
        self.active = active

    @classmethod
    def get_by_email(cls, email):
        users = db.query(cls).filter_by(email=email).all()
        return {} if len(users) < 1 else users[0]

    def save_to_db(self):
        try:
            db.add(self)
            db.commit()
        except PendingRollbackError:
            db.rollback()

        db.add(self)
        db.commit()


    @classmethod
    def get_all(cls):
        return db.query(cls).all()


class Roles(SurrogatePK, HelperMethods):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(150))
    paths: Mapped[str] = mapped_column(String(50))
