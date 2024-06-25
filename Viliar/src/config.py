from Viliar.utils import ConfigParser

conf = ConfigParser()


class Settings(object):
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Viliar REST API Developement"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = conf.database_uri
    SQLALCHEMY_TRACK_MODIFICATION = "false"
    JWT_SECRET_KEY = conf.jwt_secret_key
    JWT_TOKEN_LOCATION = 'headers'
    API_SPEC_OPTIONS = conf.api_spec_option
