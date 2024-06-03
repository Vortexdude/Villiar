from flask.views import MethodView
from . import blp
from .models import UserModel
from .params import UserLoginSchema, UserRegisterSchema


@blp.route("/login")
class LoginViews(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, data):
        user = data.__dict__
        del user['_sa_instance_state']
        return {"Status": user}


@blp.route("/register")
class RegisterViews(MethodView):
    @blp.arguments(UserRegisterSchema, location="json")
    def post(self, new_user):
        user = UserModel(**new_user)
        user.save_to_db()
        return {"data": 'data'}


@blp.route("/get_all")
class ViewUsersViews(MethodView):
    def get(self):
        users = UserModel.fetch_all()
        return {"Users": users}
