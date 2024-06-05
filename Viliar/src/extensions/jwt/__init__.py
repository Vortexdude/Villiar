from jwt import PyJWT as BaseJWT
secret = "SECRETKEY"


class JWT(BaseJWT):
    def encode(self, *args, **kwargs):
        super().encode(*args, **kwargs, key=secret, algorithm="HS256")

    def decode(self, *args, **kwargs):
        super().decode(*args, **kwargs, key=secret, algorithm="HS256")
