import sys
from typing import List


class NameErrorException(Exception):
    def __init__(self, name):
        super().__init__(f"Argument '{name}' not found in provided arguments.")


class WrongTypeCastingError(ValueError):
    def __init__(self, name, value, expected):
        super().__init__(f"Expected type '{expected}' for argument '{name}', got {type(value).__name__}.")


class UnsupportedTypeException(Exception):
    def __init__(self, type, name):
        super().__init__(f"Unsupported type '{type}' for argument '{name}'.")


class BaseParser(object):

    def __init__(self, check_env=False):
        self.check_env = check_env
        self.arguments = {}
        self.existing_args = {}
        self._args: List = sys.argv[1:]
        for full_arg in self._args:
            if '=' in full_arg:
                key, value = full_arg.split("=")
                if key.startswith('--'):
                    key = key.lstrip("--")
                if key.startswith('-'):
                    key = key.lstrip("-")
                self.existing_args.update({key: value})

    def get_args(self):
        return self.existing_args

    def add(self, name=None, type='string', alias=None, default=None):
        if not name:
            raise Exception("please pass the args name first")

        # if name not in self.existing_args.keys():
        #     raise NameErrorException(name)
        if name not in self.existing_args.keys():
            print(f"[WARNING]: Missing argument from the CLI using default {name}")
            value = default
        else:
            value = self.existing_args.get(name, default)

        if type.lower() == 'string':
            if not isinstance(value, str):
                raise WrongTypeCastingError(name, value, type.lower())
            value = str(value)

        elif type.lower() == 'bool':
            bool_types = ['true', 'false', '0', '1']
            if not isinstance(value, bool):
                if value.lower() not in bool_types:
                    raise WrongTypeCastingError(name, value, type.lower())
                if value == '0':
                    value = False
                if value == '1':
                    value = True
            value = bool(value)

        elif type.lower() == 'int':
            if not isinstance(value, int):
                try:
                    value = int(value)
                except ValueError:
                    raise WrongTypeCastingError(name, value, type.lower())
        else:
            raise UnsupportedTypeException(type, name)

        _kvi = {name: value}
        self.arguments.update(_kvi)

    def remove(self):
        pass


# bsg = BaseParser(check_env=True)
# bsg.add(name="host", type='string', default="0.0.0.0")
# bsg.add(name="port", type='int', default=582)
# bsg.add(name="debug", type='bool', default=False)
