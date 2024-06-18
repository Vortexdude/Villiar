import os


def get_env(name, default):
    return os.environ.get(name, default)


database_uri = f"postgresql://viliar:botleneck@127.0.0.1/viliar"


def database_url(driver='sqlite', host=None, username=None, password=None, database=None) -> str:
    if 'sqlite' in driver.lower():
        return "sqlite:///dev.db"
    if not host or not username or not password or not database:
        raise Exception("Please provide the sufficient credentials of the database")

    return "{}://{}:{}@{}/{}".format(driver, username, password, host, database)


class Settings(object):
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Viliar REST API Developement"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # SQLALCHEMY_DATABASE_URI = "postgresql://viliar:botleneck@db/viliar"
    SQLALCHEMY_DATABASE_URI = get_env('SQLALCHEMY_DATABASE_URI', database_url())
    SQLALCHEMY_TRACK_MODIFICATION = "false"
    JWT_SECRET_KEY = 'SECRETKEY'
    JWT_TOKEN_LOCATION = 'headers'
