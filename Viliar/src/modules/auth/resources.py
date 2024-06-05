from . import models
from sqlalchemy.exc import IntegrityError


class UserResource:
    def __init__(self, args):
        self.args = args

    def login(self):

        access_token = create_access_token(identity=self.args, fresh=True)
        refresh_token = create_refresh_token(identity=self.args)
        data = {
            "tokens": {
                "refresh_token": refresh_token,
                "access_token": access_token
            }
        }
        return {"code": 0, "msg": "success", "data": data}

    def register_user(self):
        user = models.UserModel(
            username=self.args.username,
            email=self.args.email,
            password=self.args.password,
        )
        try:
            user.save_to_db()
        except IntegrityError as e:
            return {"code": 1, "msg": "Already Exists", "data": "User is already exist."}

        return {"code": 0, "msg": "success", "data": user.email}

    @staticmethod
    def fetch_users() -> list[dict[str, str]]:
        data = models.UserModel.query.all()
        _users = [
            {
                "email": user.email,
                "username": user.username,
                "active": user.active,
                "password": user.password
            }
            for user in data
        ]
        return _users
