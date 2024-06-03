from Viliar.src.extensions.marshal import ma
from .models import UserModel


# from sqlalchemy.types import TypeDecorator, CHAR

__all__ = ["UserLoginSchema", "UserRegisterSchema"]


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
