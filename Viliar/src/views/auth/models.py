from Viliar.src.extentions.sqla import HelperMethods, Base, db, get_db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Table, Column, ForeignKey, DateTime
from uuid import uuid4
from datetime import datetime, UTC
from typing import List, Optional


def now_in_utc() -> datetime:
    """Current time in UTC"""
    return datetime.now(tz=UTC)


class SurrogatePK(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)


class UserModel(SurrogatePK):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    fullname: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_datatime: Mapped[datetime] = mapped_column(DateTime, default=now_in_utc, onupdate=now_in_utc,
                                                       nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # New field


class Roles(SurrogatePK):
    __tablename__ = 'roles'
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(150))
    paths: Mapped[str] = mapped_column(String(50))
