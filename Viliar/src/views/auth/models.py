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
        DateTime, default=now_in_utc, onupdate=now_in_utc, nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=now_in_utc, onupdate=now_in_utc, nullable=True
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
        return {} if len(users) < 1 else users[0].to_dict()

    @classmethod
    def get_by_username(cls, username):
        users = db.query(cls).filter_by(username=username).all()
        return {} if len(users) < 1 else users[0].to_dict()

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

    @staticmethod
    def update_data(current_user, fullname=None, username=None, email=None, password=None, active=None):
        current_user.fullname = fullname if fullname else current_user.fullname
        current_user.username = username if username else current_user.username
        current_user.email = email if email else current_user.email
        current_user.password = password if password else current_user.password
        current_user.active = active if active else current_user.active
        db.commit()


class Roles(SurrogatePK, HelperMethods):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(150))
    paths: Mapped[str] = mapped_column(String(50))


class BlackListToken(SurrogatePK, HelperMethods):
    __tablename__ = 'blacklist_tokens'

    token: Mapped[str] = mapped_column(String, nullable=False)
    blacklisted_on: Mapped[DateTime] = mapped_column(DateTime, default=now_in_utc, onupdate=now_in_utc, nullable=False)

    def __init__(self, token, **kwargs: Any):
        super().__init__(**kwargs)
        self.token = token

    def save_to_db(self):
        try:
            db.add(self)
            db.commit()
        except PendingRollbackError:
            db.rollback()

        db.add(self)
        db.commit()

    # def __repr__(self):
    #     return f"<id: token {self.token}>"

    def check_blacklist(self):
        res = db.query(BlackListToken).filter_by(token=self.token).all()
        return True if res else False
