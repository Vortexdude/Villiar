import toml
from flask.config import Config as FlaskConfig


class Config(FlaskConfig):
    def __init__(self, root_path=None, defaults=None, app=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.from_mapping(app.config)
        app.config = self
        return self

    def from_toml(self, filename):
        import os
        import pathlib
        filename = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve() / filename)
        try:
            with open(filename) as toml_file:
                obj = toml.load(toml_file)
        except IOError as e:
            e.strerror = "Unable to load configuration file (%s)" % e.strerror
            raise
        return self.from_mapping(obj)

    def from_mapping(self, *mapping, **kwargs):
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], "items"):
                mappings.append(mapping[0].items())
            else:
                mappings.append(mapping[0])
        elif len(mapping) > 1:
            raise TypeError(
                "expected at most 1 positional argument, got %d" % len(mapping)
            )
        mappings.append(kwargs.items())
        for mapping in mappings:
            for (key, value) in mapping:
                if key.isupper():
                    self[key] = value
        return True
