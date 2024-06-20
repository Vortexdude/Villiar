from . import blp
from flask.views import MethodView
from flask import jsonify, abort
from .models import UserModel
from .resource import UserResource, login_required
from marshmallow import Schema, fields


class UserUpdateSchema(Schema):
    email = fields.String(required=False)
    password = fields.String(required=False)
    fullname = fields.String(required=False)


class UserRegisterSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    fullname = fields.String(required=False)


class UserLoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class SomeSchemas(Schema):
    email = fields.String(required=True)


@blp.route("/users/new")
class LoginAPIView(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, args):
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
        for arg in args:
            if not isinstance(arg, dict) or not arg:
                return jsonify({"status": "No data found"}), 203
            new_data = arg
        current_user = kwargs['current_user'] if 'current_user' in kwargs else object
        username: str = kwargs['username'] if 'username' in kwargs else ''
        user = UserResource.get_by_username(username)
        if not user:
            return jsonify({"status": "Username not matched"}), 203
        # UserResource.update_data(identity, **new_data)
        return {"data": "looks good."}
        # return user


@blp.route("/login")
class LoginUserViews(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, args):
        if 'email' not in args or 'password' not in args:
            abort(407, 'Please provide the email and password')

        user = UserModel.get_by_email(args['email'])
        if not user:
            abort(404, 'User does not exist in the database')

        return UserResource(args).login(user.password)


@blp.route("/logout")
class LogoutView(MethodView):

    @login_required(omit_token=True)
    def post(self, token: str):
        return UserResource.logout(token)
