from . import blp
from flask.views import MethodView
from flask import jsonify, abort
from .models import UserModel

from marshmallow import Schema, fields


class UserRegisterSchema(Schema):
    username = fields.String(required=True)


@blp.route("/register")
class RegisterUserViews(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, args):
        user = UserModel(
            username=args['username']
        )
        print(user.save_to_db())

        return jsonify({"data": "dfasta"})


@blp.route("/login")
class LoginUserViews(MethodView):

    def post(self):
        return jsonify({"Statu": "Done"})
