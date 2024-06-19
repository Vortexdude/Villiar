import os


class ConfigParser(object):
    @staticmethod
    def _get_env(key: str, default: str) -> int | str:
        return os.environ.get(key, default)

    @property
    def database_uri(self):
        POSTGRES = {
            'user': self._get_env('POSTGRES_USER', 'viliar'),
            'pw': self._get_env('POSTGRES_PASSWORD', 'botleneck'),
            'host': self._get_env('POSTGRES_HOST', '127.0.0.1'),
            'db': self._get_env('POSTGRES_DB', 'viliar'),
        }
        if not POSTGRES['user']:
            return self._get_env("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
        SQLALCHEMY_DATABASE_URI = "postgresql://%(user)s:%(pw)s@%(host)s/%(db)s" % POSTGRES
        # os.environ['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        return SQLALCHEMY_DATABASE_URI

    @property
    def jwt_secret_key(self):
        return self._get_env('JWT_SECRET_KEY', 'supersecret')

    @property
    def api_spec_option(self):
        data = {'security': [{"bearerAuth": []}], 'components': {
            "securitySchemes":
                {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
        }}
        return data


class Settings(object):
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Viliar REST API Developement"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = ConfigParser().database_uri
    SQLALCHEMY_TRACK_MODIFICATION = "false"
    JWT_SECRET_KEY = ConfigParser().jwt_secret_key
    JWT_TOKEN_LOCATION = 'headers'
    API_SPEC_OPTIONS = ConfigParser().api_spec_option
