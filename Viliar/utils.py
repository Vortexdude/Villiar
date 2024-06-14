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
            raise Exception("please pass the args name first")

        if name not in self.cli_arg.keys():
            print(f"[WARNING]: Missing argument from the CLI using default {name} value {default}")
            value = default
        else:
            value = self.cli_arg.get(name, default)

        value = validate_argument(name=name, expected_type=type, value=value)

        _kvi = {name: value}
        self.arguments.update(_kvi)
