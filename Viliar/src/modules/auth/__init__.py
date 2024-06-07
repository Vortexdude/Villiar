from flask_smorest import Blueprint
from Viliar.src.extensions.api import api
blp = Blueprint("Auth", __name__,  description="auth Section")

blp.DEFAULT_LOCATION_CONTENT_TYPE_MAPPING = {
    "json": "application/json",
    "form": "application/x-www-form-urlencoded",
    "files": "multipart/form-data",
}


def init_app(app):
    from . import views
    api.register_blueprint(blp=blp)
