from Viliar.src.extentions.sqla import HelperMethods, Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from uuid import uuid4
from datetime import datetime, UTC
from typing import List


def now_in_utc() -> datetime:
    """Current time in UTC"""
    return datetime.now(tz=UTC)


user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', ForeignKey('public.users.id'), primary_key=True),
    Column('role_id', ForeignKey('public.roles.id'), primary_key=True),
    schema='public'
)

# Association table between roles and policies
role_policies = Table(
    'role_policies', Base.metadata,
    Column('role_id', ForeignKey('public.roles.id'), primary_key=True),
    Column('policy_id', ForeignKey('public.policies.id'), primary_key=True),
    schema='public'
)


class SurrogatePK(Base):
    __abstract__ = True
    id: Mapped[str] = mapped_column(String, default=lambda: str(uuid4()), primary_key=True)


class UserModel(SurrogatePK, HelperMethods):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        nullable=False,
        default=now_in_utc,
        onupdate=now_in_utc
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    roles: Mapped[List["Role"]] = relationship("Role", secondary=user_roles, back_populates="users")

    def __init__(self, username):
        super().__init__()
        self.username = username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Role(SurrogatePK, HelperMethods):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String, unique=True)
    users: Mapped[List["UserModel"]] = relationship("UserModel", secondary=user_roles, back_populates="roles")
    policies: Mapped[List["Policy"]] = relationship("Policy", secondary=role_policies, back_populates="roles")


class Policy(SurrogatePK, HelperMethods):
    __tablename__ = 'policies'

    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)
    roles: Mapped[List["Role"]] = relationship("Role", secondary=role_policies, back_populates="policies")



