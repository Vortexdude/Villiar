from flask.views import MethodView
from . import blp


@blp.route("/server")
class MonitorServerViews(MethodView):

    def get(self):
        return {"data": "Nothing"}
