from flask import Flask
from .api import api
from .sqla import db
extensions = [api, db]


def init_app(app: Flask):
    for ext in extensions:
        with app.app_context():
            db.init_app(ext)
    api.init_app(app)
