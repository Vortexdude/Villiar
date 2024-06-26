from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Employee


class EmployeeSchema(SQLAlchemySchema):
    class Meta:
        model = Employee
        load_instance = True
