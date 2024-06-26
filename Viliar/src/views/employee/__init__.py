from flask_smorest import Blueprint
from flask import Flask
from Viliar.src.extentions.api import api

blp = Blueprint("Employee", __name__, description="Auth Operations")


def register_blp(app: Flask):
    from . import routes
    api.register_blueprint(blp)
