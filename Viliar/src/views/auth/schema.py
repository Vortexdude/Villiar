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
