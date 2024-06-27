from . import blp
from flask.views import MethodView
from .models import db, Address, Employee, Designation
from .schema import EmployeeOnboardSchema
from .resource import EmployeeResource


@blp.route("/onboard_employee")
class EmployeeView(MethodView):
    @blp.arguments(EmployeeOnboardSchema)
    def post(self, args: EmployeeOnboardSchema):
        return EmployeeResource(args).oboard()

    def get(self):
        for employee in EmployeeResource.get_all():
            employee_dict = employee.to_dict()
            return employee_dict
