from jwt import PyJWT as BaseJWT
from Viliar.src.config import ConfigParser


class JWT(BaseJWT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self, *args, **kwargs):
        return super().encode(*args, **kwargs, key=ConfigParser().jwt_secret_key, algorithm='HS256')

    def decode(self, *args, **kwargs):
        return super().decode(*args, **kwargs, key=ConfigParser().jwt_secret_key, algorithms=['HS256'])


jwt = JWT()
