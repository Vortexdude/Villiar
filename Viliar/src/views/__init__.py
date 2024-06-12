def register_blueprints(app):
    from importlib import import_module

    modules = app.config['ENABLED_MODULES']

    for modulename in modules:
        module = import_module(f"Viliar.src.views.{modulename}", "app")
        module.register_blp(app)
