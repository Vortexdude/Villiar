from . import blp
from flask.views import MethodView


@blp.route("/")
class EmployeeView(MethodView):
    def get(self):
        return {"data": "success"}
