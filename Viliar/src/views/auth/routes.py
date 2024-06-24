from . import blp
from flask.views import MethodView
from flask import jsonify, abort
from .models import UserModel
from .resource import UserResource, login_required
from .schema import UserLoginSchema, UserRegisterSchema, UserUpdateSchema


@blp.route("/users/new")
class LoginAPIView(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, args):
        """Register new user"""
        user = UserResource(args)
        new_user = user.register()
        return jsonify(new_user)


@blp.route("/users/<string:username>")
class FetchUsersViews(MethodView):

    @login_required()
    def get(self, username, current_user: UserModel):
        """For fetch the specific user from the database"""
        if not username:
            return jsonify({"message": "Please provide the username"}, 203)
        users: dict = UserResource.get_by_username(username)
        return jsonify({"User": users})

    @blp.arguments(UserUpdateSchema)
    @login_required()
    def post(self, *args, **kwargs):
        """Update the given user Information"""
        new_data = {}
        for arg in args:
            if not isinstance(arg, dict) or not arg:
                return jsonify({"status": "No data found"}), 203
            new_data = arg
        current_user = kwargs['current_user'] if 'current_user' in kwargs else object
        username: str = kwargs['username'] if 'username' in kwargs else ''
        user = UserResource.get_by_username(username)
        if not user:
            return jsonify({"status": "Username not matched"}), 203
        new_data['username'] = username
        UserResource.update_data(**new_data)
        return UserResource.get_by_username(username)


@blp.route("/login")
class LoginUserViews(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, args):
        """Login route for the user"""
        if 'email' not in args or 'password' not in args:
            abort(407, 'Please provide the email and password')
        user = UserModel.get_by_email(args['email'], populate_pass=True)
        if not user:
            abort(404, 'User does not exist in the database')

        return UserResource(args).login(user['password'])


@blp.route("/logout")
class LogoutView(MethodView):

    @login_required(omit_token=True)
    def post(self, token: str):
        """Logout the user add token in the blacklist table"""
        return UserResource.logout(token)
