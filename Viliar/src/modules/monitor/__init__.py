from flask_smorest import Blueprint
from Viliar.src.extensions.api import api
blp = Blueprint("Monitor", __name__, description="Monitor Section", url_prefix="/api/v1")


def init_app(app):
    from . import views
    api.register_blueprint(blp)
