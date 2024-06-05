from jwt import PyJWT as BaseJWT
secret = "SECRETKEY"


class JWT(BaseJWT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self, *args, **kwargs):
        return super().encode(*args, **kwargs, key=secret, algorithm="HS256")

    def decode(self, *args, **kwargs):
        return super().decode(*args, **kwargs, key=secret, algorithms=["HS256"])


jwt = JWT()
