from flask_smorest import Blueprint
from Viliar.src.extensions.api import api
blp = Blueprint("Auth", __name__,  description="auth Section")


def init_app(app):
    from . import views
    api.register_blueprint(blp=blp)
