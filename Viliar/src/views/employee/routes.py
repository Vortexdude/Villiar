from . import blp
from flask.views import MethodView
from .schema import EmployeeOnboardSchema, EmployeeUpdateSchema
from .resource import EmployeeResource


@blp.route("/employee/<string:name>")
class EmployeeView(MethodView):

    def get(self, name=""):
        """For fetch the particular employee from the database"""
        return EmployeeResource.get_one(name)

    @blp.arguments(EmployeeOnboardSchema)
    def post(self, args: EmployeeOnboardSchema, name=""):
        """Onboard the employee"""
        return EmployeeResource(args).oboard(name)

    @blp.arguments(EmployeeUpdateSchema)
    def patch(self, args: EmployeeOnboardSchema, name=""):
        """Update the employee details"""
        return EmployeeResource(args).update(name)

    def delete(self, name=""):
        """off board employee"""
        return EmployeeResource.discard(name)
        # return {"Status": "Success"}, 203
