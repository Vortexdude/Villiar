from Viliar.src.extensions.flask import Flask
from Viliar.src.extensions import init_app

CONFIG_MAPPING = {
    'development': 'config/development.toml',
    'production': 'config/production.toml',
    'testing': 'config/testing.toml'

}


def register_modules(app):
    from Viliar.src import modules
    modules.init_app(app)


def create_app(config='development'):
    app = Flask(__name__)
    app.config.from_toml(CONFIG_MAPPING[config])
    init_app(app)
    register_modules(app)
    return app
