from . import models
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, UTC
from Viliar.src.extensions.jwt import jwt
from Viliar.src.extensions.jwt.exceptions import ExpiredSignatureError, DecodeError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, abort


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization", None)
        if not authorization:
            abort(403, description='no authorization token provided')

        auth_type, token = authorization.split(' ')
        if "Bearer" not in auth_type:
            abort(403, description="Token type should be bearer")
        try:
            decoded_token = jwt.decode(token)
            current_user = models.UserModel.get_by_email(email=decoded_token['identity'])
            return f(*args, **kwargs, current_user=current_user)

        except ExpiredSignatureError as e:
            abort(401, description="Token expired or invalid")

        except DecodeError as e:
            abort(400, description="Bad Request")

    return wrapper


class UserResource:
    def __init__(self, args):
        self.args = args

    def login(self, password):

        if not check_password_hash(password, self.args.password):
            return {"code": 0, "msg": "error", "data": "Entered credentials are not correct"}

        payload = {
            "identity": self.args.email,
            "exp": datetime.now(UTC) + timedelta(minutes=30)
        }
        token = jwt.encode(payload)
        data = {
            "access_token": token
        }
        return {"code": 0, "msg": "success", "data": data}

    def register_user(self):
        hashed_password = generate_password_hash(self.args.password)
        user = models.UserModel(
            username=self.args.username,
            email=self.args.email,
            password=hashed_password,
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
                "active": user.active
            }
            for user in data
        ]
        return _users
