from flask.views import MethodView
from . import blp
from .params import MonitorServerSchema
from .resource import read_os_release


@blp.route("/server")
class MonitorServerViews(MethodView):

    @blp.arguments(MonitorServerSchema, location="query")
    def get(self, args):
        if 'os-release' in args['entity']:
            return read_os_release()
        else:
            return {"status": "Need to add more"}
