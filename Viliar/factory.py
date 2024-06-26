from flask import Flask
from Viliar.src.config import Settings
from Viliar.src.extentions import init_app
from Viliar.src.views import register_blueprints

MODULES = ['auth', 'employee']


def create_app(modules, config=None):
    """Instance the app."""
    app = Flask(__name__)
    app.config.from_object(Settings)
    app.config['ENABLED_MODULES'] = modules
    init_app(app)
    register_blueprints(app)

    return app
