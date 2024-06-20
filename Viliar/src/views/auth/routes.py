from . import blp
from flask.views import MethodView
from flask import jsonify, abort
from .models import UserModel
from .resource import UserResource, login_required
from marshmallow import Schema, fields


class UserRegisterSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    fullname = fields.String(required=False)


class UserLoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


@blp.route("/register")
class RegisterUserViews(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, args):
        user = UserResource(args)
        new_user = user.register()
        return jsonify(new_user)


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


@blp.route("/get_all")
class FetchUsersViews(MethodView):

    @login_required
    def post(self, current_user: UserModel):
        print(current_user.email)
        users: list = UserResource.get_all()
        return jsonify({"Users": users})
