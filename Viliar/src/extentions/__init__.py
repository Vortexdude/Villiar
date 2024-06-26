from flask import Flask
from .api import api
from .sqla import db, Base

extensions = [api, db]


def init_app(app: Flask):
    with app.app_context():
        db.init_app(app)

    for ext in extensions:
        pass
    api.init_app(app)
