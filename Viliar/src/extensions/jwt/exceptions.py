from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import DecodeError


class SignatureExpired(ExpiredSignatureError):
    """Raised when signature is expired"""
    pass
