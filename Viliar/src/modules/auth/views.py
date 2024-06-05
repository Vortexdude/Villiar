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

        return UserResource(args).login(user.password)


@blp.route("/me")
class Identity(MethodView):

    @blp.doc(parameters=[body])
    @login_required
    def get(self, current_user):
        return {"data": current_user.to_json()}


@blp.route("/register")
class RegisterViews(MethodView):
    @blp.arguments(UserRegisterSchema, location="json")
    def post(self, args):
        return UserResource(args).register_user()


@blp.route("/get_all")
class ViewUsersViews(MethodView):
    # @blp.doc(parameters=[body])
    @blp.arguments(AuthSchema, location='headers')
    def get(self):
        return UserResource.fetch_users()
