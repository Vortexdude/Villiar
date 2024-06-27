from Viliar.src.extentions.sqla import get_db, SurrogatePK, HelperMethods, now_in_utc
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer, ForeignKey
from datetime import datetime
from typing import List
from sqlalchemy.exc import PendingRollbackError
db = next(get_db())


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


class Employee(SurrogatePKExtended, HelperMethods):
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    joining_date: Mapped[datetime] = mapped_column(DateTime, default=now_in_utc, nullable=False)
    total_experience: Mapped[int] = mapped_column(Integer, nullable=False)

    # Foreign_keys
    designation_id: Mapped[str] = mapped_column(String, ForeignKey("designations.id"), nullable=False)
    address_id: Mapped[str] = mapped_column(String, ForeignKey("addresses.id"), nullable=False)

    # relationships
    designation: Mapped["Designation"] = relationship("Designation", back_populates="employees")
    address: Mapped["Address"] = relationship("Address", back_populates="employees")

    def __init__(self, name, salary, total_experience, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.salary = salary
        self.total_experience = total_experience

    def __repr__(self):
        return f"<Employee {self.name}, with salary of {self.salary} and experience {self.total_experience}>"


class Address(SurrogatePKExtended):
    __tablename__ = 'addresses'

    street: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    state: Mapped[str] = mapped_column(String(30), nullable=True)
    zip_code: Mapped[str] = mapped_column(String(10), nullable=True)
    employees: Mapped[List["Employee"]] = relationship('Employee', back_populates="address")

    def __init__(self, street, city, state, zip_code, **kwargs):
        super().__init__(**kwargs)
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self):
        return f"<Address {self.street}, {self.city}>"


class Designation(SurrogatePKExtended):
    __tablename__ = 'designations'

    title: Mapped[str] = mapped_column(String(100), nullable=True)
    employees: Mapped[List["Employee"]] = relationship('Employee', back_populates="designation")

    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.title = title

    @classmethod
    def get_all(cls) -> list:
        return db.query(cls).all()

    @classmethod
    def get_by_name(cls, name):
        return db.query(cls).filter_by(title=name).first()

    def __repr__(self):
        return f"<Designation {self.title}>"


class Project(SurrogatePK):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(50))
