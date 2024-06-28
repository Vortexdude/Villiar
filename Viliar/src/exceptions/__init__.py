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


class UserAlreadyExistException(Exception):

    def __init__(self):
        super().__init__("User already exists")


class UserNotExistException(Exception):

    def __init__(self):
        super().__init__("User not exists")


class FormatterError(Exception):
    def __init__(self):
        super().__init__("Address must be in formatted manner")


class AttributeNotFound(Exception):
    def __init__(self, attribute):
        super().__init__(f"{attribute} not found in the database")
