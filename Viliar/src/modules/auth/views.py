from flask.views import MethodView
from flask_smorest import abort
from .resources import UserResource, login_required
from . import blp, models
from .params import UserLoginSchema, UserRegisterSchema, AuthSchema

body = {
    'name': 'Authorization',
    'in': 'header',
    'description': 'Authorization Bearer <access_token>',
    'required': 'true',
    'default': "nothing",
}


@blp.route("/create_admin_user")
class RoleView(MethodView):
    @blp.arguments(UserRegisterSchema, location="json")
    def post(self, args):
        if args.email is None or args.password is None:
            abort(404, message="Required email and password for Creation")

        user = models.UserModel.get_by_email(args.email)

        if user:
            abort(403, message="User is already exists")

        return UserResource(args).create_admin_user()


@blp.route("/login")
class LoginViews(MethodView):
    @blp.arguments(UserLoginSchema)
    @blp.response(404, description="User Does not exist")
    @blp.response(403, description="User password is wrong")
    @blp.response(407, description="User is not activated")
    def post(self, args):
        if args.email is None or args.password is None:
            abort(404, message="Required email and password for login")

        user = models.UserModel.get_by_email(args.email)

        if not user:
            abort(403, message="Please Enter the correct email.")

        if not user.active:
            abort(407, message="User is not active.")

        return UserResource(args).login(user.password)


@blp.route("/me")
class Identity(MethodView):

    @blp.doc(parameters=[body])
    @blp.response(403, description="no authorization token provided")
    @blp.response(401, description="Invalid token")
    @blp.response(200, description="Get Identity")
    @login_required
    def get(self, current_user):
        return {"data": current_user.to_json()}, 200


@blp.route("/register")
class RegisterViews(MethodView):
    @blp.arguments(UserRegisterSchema, location="json")
    def post(self, args):
        return UserResource(args).register_user()


@blp.route("/get_all")
class ViewUsersViews(MethodView):
    @blp.doc(parameters=[body])
    @blp.response(403, description="no authorization token provided")
    @blp.response(401, description="Invalid token")
    @login_required
    def get(self, current_user):
        return UserResource.fetch_users(), 200
