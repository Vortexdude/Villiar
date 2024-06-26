from . import blp
from flask.views import MethodView
from .models import Address, Employee, Designation
from .models import db


@blp.route("/onboard_employee")
class EmployeeView(MethodView):
    def post(self):
        return {"data": "success"}

    def get(self):
        for employee in db.query(Employee).all():
            print(employee.designation.title)
        return {"data": "done"}
