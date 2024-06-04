from .api import api, spec_kwargs
from .sqla import db
from .marshal import ma
from .jwt import jwt


def init_app(app):
    for ext in [db, ma, jwt]:
        ext.init_app(app)
        # with app.app_context():
        #     db.create_all()
    api.init_app(app, spec_kwargs=spec_kwargs)
