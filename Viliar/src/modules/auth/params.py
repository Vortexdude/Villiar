from Viliar.src.extensions.marshal import ma
from .models import UserModel
from marshmallow import Schema, fields

# from sqlalchemy.types import TypeDecorator, CHAR

__all__ = ["UserLoginSchema", "UserRegisterSchema", "AuthSchema"]


class BaseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        include_relationships = True
        load_instance = True

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("users.user_detail", user_id="<id>"),
            "collection": ma.URLFor("users.users"),
        }
    )


class UserLoginSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        #  Fields that need to be shown
        fields = ("email", "password")


class UserRegisterSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        #  Fields that need to be shown
        fields = ("username", "email", "password")


class AuthSchema(Schema):
    Authorization = fields.Str(required=True, description="JWT token in the form of 'Bearer <token>'")
