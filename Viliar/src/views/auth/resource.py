from Viliar.src.extentions.jwt import jwt
from .models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from jwt import encode, decode, ExpiredSignatureError, DecodeError
from datetime import datetime, UTC, timedelta
from functools import wraps
from flask import request, abort
from .models import BlackListToken


def login_required(omit_token=False):
    def main_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            headers = request.headers.get('Authorization', None)

            if not headers or len(headers.split(" ")) > 2:
                abort(403, description='no authorization token provided')

            token_type, token_data = headers.split(" ")
            identity = jwt.decode(token_data)

            if "Bearer" not in token_type:
                abort(403, description="Token type should be bearer")

            try:
                if BlackListToken(token_data).check_blacklist():
                    abort(401, description="Token is blacklisted please login again")

                identity = jwt.decode(token_data)
                current_user = UserModel.get_by_email(email=identity['identity'])
                if omit_token:
                    return f(*args, **kwargs, token=token_data)
                return f(*args, **kwargs, current_user=current_user)

            except ExpiredSignatureError as e:
                abort(401, description="Token expired or invalid")

            except DecodeError as e:
                abort(400, description="Bad Request")
        return wrapper
    return main_wrapper


class UserResource(object):
    def __init__(self, args: dict):
        self.args = args

    def register(self):
        self.args['password'] = generate_password_hash(self.args['password'])
        new_user = UserModel(**self.args)
        try:
            new_user.save_to_db()
        except IntegrityError as e:
            return {"code": 1, "msg": "Already Exists", "data": "User is already exist."}

        return {"code": 0, "msg": "success", "data": new_user.email}

    def login(self, password):
        if not check_password_hash(password, self.args['password']):
            return {"code": 0, "msg": "error", "data": "Entered credentials are not correct"}, 400

        payload = {
            "identity": self.args['email'],
            "exp": datetime.now(tz=UTC) + timedelta(minutes=30)
        }
        token = jwt.encode(payload)
        data = {
            "access_token": token
        }
        return {"code": 0, "msg": "success", "data": data}, 200

    @staticmethod
    def logout(token):
        try:
            blacklist_token = BlackListToken(token=token)
            blacklist_token.save_to_db()
            return {'status': 'success', 'message': 'Successfully logged out.'}
        except Exception as e:
            abort(500, "Unknown Error from database side")

    @staticmethod
    def get_all():
        users = UserModel.get_all()
        _users = [
            {
                k: v for k, v in user.items()
                if (k != 'password' and k != 'id')
            }
            for user in [
                user.to_dict() for user in users
            ]
        ]
        return _users
