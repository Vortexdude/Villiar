import os
import sys
from typing import List
from abc import ABC


class NameErrorException(Exception):
    def __init__(self, name):
        super().__init__(f"Argument '{name}' not found in provided arguments.")


class WrongTypeCastingError(ValueError):
    def __init__(self, name, value, expected_type):
        self.name = name
        self.value = value
        self.expected_type = expected_type

        super().__init__(f"Cannot cast {name} (value: {value}) to {expected_type}")


class UnsupportedTypeException(Exception):
    def __init__(self, expected_type, name):
        self.expected_type = expected_type
        self.name = name
        super().__init__(f"Unsupported type {expected_type} for argument {name}")


class BaseAbstract(ABC):
    arguments = {}

    def add(self):
        """ Add new arguments in the cli to"""
        pass


def validate_argument(name, expected_type, value) -> int | str | bool:
    """
    Validate and cast the argument value to the expected type.

    Args:
        name (str): The name of the argument.
        expected_type (str): The expected type of the argument ('string', 'int', or 'bool').
        value (any): The value of the argument to validate and cast.

    Returns:
        int | str | bool: The value cast to the expected type.

    Raises:
        WrongTypeCastingError: If the value cannot be cast to the expected type.
        UnsupportedTypeException: If the expected type is not supported.
    """

    if expected_type.lower() == 'string':
        if not isinstance(value, str):
            raise WrongTypeCastingError(name, value, expected_type.lower())
        return str(value)

    elif expected_type.lower() == 'int':
        if not isinstance(value, int):
            try:
                return int(value)
            except ValueError:
                raise WrongTypeCastingError(name, value, expected_type.lower())

    elif expected_type.lower() == 'bool':
        if isinstance(value, bool):
            return bool(value)

        bool_str_mapping = {
            'true': True,
            'false': False,
            '0': False,
            '1': True
        }
        value_str = str(value).lower()
        if value_str in bool_str_mapping:
            return bool_str_mapping[value_str]
        else:
            raise WrongTypeCastingError(name, value, expected_type)

    else:
        raise UnsupportedTypeException(expected_type, name)


class BaseParser(BaseAbstract):

    def __init__(self, check_env=False):
        self.check_env = check_env
        self.arguments = {}
        self.cli_arg = {}
        self._args: List = sys.argv[1:]
        for full_arg in self._args:
            if '=' in full_arg:
                key, value = full_arg.split("=")
                if key.startswith('--'):
                    key = key.lstrip("--")
                if key.startswith('-'):
                    key = key.lstrip("-")
                self.cli_arg.update({key: value})

    def get_args(self):
        return self.cli_arg

    def add(self, name=None, type='string', alias=None, default=None):
        if not name:
            raise Exception("Please pass the argument name first.")

        value = default

        if name in self.cli_arg.keys():
            value = self.cli_arg.get(name)
            if not value:
                value = default

        elif self.check_env:
            value = os.environ.get(name, default)
        try:
            value = validate_argument(name=name, expected_type=type, value=value)
        except (WrongTypeCastingError, UnsupportedTypeException) as e:
            print(f"[Error] {e} using default {default} type of value is")
            value = default

        _kvi = {name: value}
        self.arguments.update(_kvi)


class ConfigParser(object):

    def __init__(self):
        self._admin_pass = self._get_env('ADMIN_PASS', 'secret')
        self._guest_pass = self._get_env('GUEST_PASS', 'supersecret')
        self._jwt_secret_key = self._get_env('JWT_SECRET_KEY', 'supersecret')
        self._pg_user = self._get_env('POSTGRES_USER', 'viliar')
        self._pg_pass = self._get_env('POSTGRES_PASSWORD', 'botleneck')
        self._pg_db = self._get_env('POSTGRES_DB', 'viliar')
        self._pg_host = self._get_env('POSTGRES_HOST', '127.0.0.1')
        basedir = os.path.abspath(os.path.dirname(__file__))
        self._sqlite_uri = 'sqlite:///' + os.path.join(basedir, 'database.db')

    @staticmethod
    def _get_env(key: str, default: str) -> int | str:
        return os.environ.get(key, default)

    @property
    def admin_pass(self) -> str:
        return self._admin_pass

    @property
    def guest_pass(self) -> str:
        return self._guest_pass

    @property
    def jwt_secret_key(self) -> str:
        return self._jwt_secret_key

    @property
    def database_uri(self):
        POSTGRES = {
            'user': self._pg_user,
            'pw': self._pg_pass,
            'host': self._pg_host,
            'db': self._pg_db,
        }
        if not POSTGRES['user']:
            return self._get_env("SQLALCHEMY_DATABASE_URI", self._sqlite_uri)
        SQLALCHEMY_DATABASE_URI = "postgresql://%(user)s:%(pw)s@%(host)s/%(db)s" % POSTGRES
        # os.environ['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        return SQLALCHEMY_DATABASE_URI

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

