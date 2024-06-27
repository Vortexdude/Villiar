from . import blp
from flask.views import MethodView
from .schema import EmployeeOnboardSchema
from .resource import EmployeeResource


@blp.route("/employee")
class EmployeeView(MethodView):
    @blp.arguments(EmployeeOnboardSchema)
    def post(self, args: EmployeeOnboardSchema):
        return EmployeeResource(args).oboard()

    def get(self):
        return EmployeeResource.get_all()

    def delete(self):
        return {"Status": "Success"}, 203
