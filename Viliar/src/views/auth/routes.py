from . import blp
from flask.views import MethodView


@blp.route("/register")
class RegisterUserViews(MethodView):
    def get(self):
        return {"data": "dfasta"}

