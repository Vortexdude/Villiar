from flask.views import MethodView
from .resources import UserResource
from flask_smorest import abort
from . import blp, models
from .params import UserLoginSchema, UserRegisterSchema


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)


def get_password_hash(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")


@blp.route("/login")
class LoginViews(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, args):
        print(f"{args.password=}")
        if args.email is None or args.password is None:
            abort(404, message="Required email and password for login")

        user = models.UserModel.get_by_email(args.email)

        if not user:
            abort(404, message="Please Enter the correct email.")

        if not user.active:
            abort(403, message="User is not active.")

        if not check_password(user.password, args.password):
            abort(401, message="User is not authenticate")

        return UserResource(args).login()


@blp.route("/register")
class RegisterViews(MethodView):
    @blp.arguments(UserRegisterSchema, location="json")
    def post(self, args):
        args.password = get_password_hash(args.password)
        return UserResource(args).register_user()


@blp.route("/get_all")
class ViewUsersViews(MethodView):
    def get(self):
        return UserResource.fetch_users()
