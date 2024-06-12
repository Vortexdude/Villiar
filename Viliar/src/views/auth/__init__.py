from flask import Flask
from flask_smorest import Blueprint
from Viliar.src.extentions.api import api

blp = Blueprint("Auth", __name__, url_prefix='/auth', description="Auth Operations")


def register_blp(app: Flask):
    from . import routes
    api.register_blueprint(blp)
