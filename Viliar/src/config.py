class Settings(object):
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Viliar REST API Developement"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = "postgresql://viliar:botleneck@db/viliar"
    SQLALCHEMY_TRACK_MODIFICATION = "True"
    JWT_SECRET_KEY = 'SECRETKEY'
    JWT_TOKEN_LOCATION = 'headers'
