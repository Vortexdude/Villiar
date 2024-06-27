from Viliar.src.extentions.sqla import HelperMethods, Base, get_db, SurrogatePK, now_in_utc
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Table, Column, ForeignKey, DateTime
from datetime import datetime
from typing import List, Optional, Any
from sqlalchemy.exc import PendingRollbackError
db = next(get_db())

role_associations = Table(
    'role_associations',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id'), primary_key=True),
    Column('role_id', String, ForeignKey('roles.id'), primary_key=True)
)


class SurrogatePKExtended(SurrogatePK):
    __abstract__ = True

    def save_to_db(self):
        try:
            db.add(self)
            db.commit()
        except PendingRollbackError:
            db.rollback()

        db.add(self)
        db.commit()


class Role(SurrogatePKExtended, HelperMethods):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(150))
    paths: Mapped[str] = mapped_column(String(50))
    users: Mapped[List["UserModel"]] = relationship(
        "UserModel", secondary=role_associations, back_populates='roles'
    )

    def __init__(self, name, description, paths, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.paths = paths

    def __repr__(self):
        return f"<Role {self.name} and description {self.description}>"


class UserModel(SurrogatePKExtended, HelperMethods):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    fullname: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_datatime: Mapped[datetime] = mapped_column(
        DateTime, default=now_in_utc, nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=now_in_utc, onupdate=now_in_utc, nullable=False
    )

    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary=role_associations, back_populates='users'
    )

    def __init__(self, username, email, password, active=True, fullname=None, **kw: Any):
        super().__init__(**kw)
        self.fullname = fullname if fullname else username
        self.username = username
        self.email = email
        self.password = password
        self.active = active

    def __repr__(self):
        return f"<User {self.username} and email {self.email}>"

    @classmethod
    def get_by_email(cls, email, populate_pass=False, obj=False) -> object | dict:
        user = db.query(cls).filter_by(email=email).first()
        if user:
            return user if obj else user.to_dict(populate_pass)
        else:
            return {}

    @classmethod
    def get_by_username(cls, username, populate_pass=False, obj=False) -> object | dict:
        user = db.query(cls).filter_by(username=username).first()
        if user:
            return user if obj else user.to_dict(populate_pass)
        else:
            return {}

    @classmethod
    def login(cls, email):
        user = cls.get_by_email(email=email, obj=True)
        print(now_in_utc())
        user.last_login = now_in_utc()
        db.commit()

    @classmethod
    def get_all(cls):
        return db.query(cls).all()

    @classmethod
    def update_data(cls, fullname=None, username=None, email=None, password=None, active=None):
        from werkzeug.security import generate_password_hash
        current_user = db.query(cls).filter_by(username=username).first()
        current_user.fullname = fullname if fullname else current_user.fullname
        current_user.username = username if username else current_user.username
        current_user.email = email if email else current_user.email
        current_user.password = generate_password_hash(password) if password else current_user.password
        current_user.active = active if active else current_user.active

        try:
            db.commit()
        except Exception as e:
            raise Exception("Error with the database.")


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
