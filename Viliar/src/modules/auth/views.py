from flask.views import MethodView
from .resources import UserResource
from flask_smorest import abort
from . import blp, models
from .params import UserLoginSchema, UserRegisterSchema
from .params import AuthSchema
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request
import jwt


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization", None)
        if not authorization:
            abort(403, message='no authorization token provided')

        auth_type, token = authorization.split(' ')
        if "Bearer" not in auth_type:
            abort(403, message="Token type should be bearer")
        try:
            decoded_token = jwt.decode(token, "SECRETKEY", algorithms="HS256")
            current_user = models.UserModel.get_by_email(email=decoded_token['identity'])
            return f(*args, **kwargs, current_user=current_user)

        except Exception as e:
            abort(401, message="Invalid or expired token")

    return wrapper


body = {
    'name': 'Authorization',
    'in': 'header',
    'description': 'Authorization: Bearer <access_token>',
    'required': 'true',
    'default': "nothing",
    'schema': {'type': 'string'}
}
timeout_field = {
    'name': 'timeout',
    'in': 'header',
    'description': '3000 #paste your timeout session',
    'required': 'true',
    'default': "3000"
}


@blp.route("/login")
class LoginViews(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, args):
        if args.email is None or args.password is None:
            abort(404, message="Required email and password for login")

        user = models.UserModel.get_by_email(args.email)

        if not user:
            abort(404, message="Please Enter the correct email.")

        if not user.active:
            abort(403, message="User is not active.")
        import datetime
        from datetime import timedelta

        if check_password_hash(user.password, args.password):
            payload = {
                "identity": args.email,
                "exp": datetime.datetime.now(datetime.UTC) + timedelta(minutes=30)
            }
            token = jwt.encode(payload, "SECRETKEY", algorithm="HS256")
            data = {
                "access_token": token
            }
            return {"code": 0, "msg": "success", "data": data}


@blp.route("/me")
class Identity(MethodView):
    @login_required
    def get(self, current_user):
        print(current_user)
        return {"data": current_user}


@blp.route("/register")
class RegisterViews(MethodView):
    @blp.arguments(UserRegisterSchema, location="json")
    def post(self, args):
        args.password = generate_password_hash(args.password)
        return UserResource(args).register_user()


@blp.route("/get_all")
class ViewUsersViews(MethodView):
    @blp.doc(parameters=[body])
    # @blp.arguments(AuthSchema, location='headers')
    def get(self):
        return UserResource.fetch_users()
