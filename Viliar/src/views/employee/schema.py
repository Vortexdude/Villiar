from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from .models import Employee
from marshmallow import Schema, fields


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_relationships = True
        include_fk = True
        exclude = ("id", "designation_id", "address_id", "joining_date")

    address = auto_field()


class EmployeeOnboardSchema(Schema):
    name = fields.String(required=True)
    salary = fields.Integer(required=True)
    total_experience = fields.Integer(required=True)
    designation = fields.String(required=True)
    address = fields.String(required=True)
