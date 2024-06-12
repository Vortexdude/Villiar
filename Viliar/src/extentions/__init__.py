from flask import Flask
from .api import api
from .sqla import db, Base
from sqlalchemy import create_engine

extensions = [api, db]


def init_app(app: Flask):
    # engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    # Base.metadata.create_all(engine)
    with app.app_context():
        db.init_app(app)

    for ext in extensions:
        pass
    api.init_app(app)
