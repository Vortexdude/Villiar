from flask_marshmallow import Marshmallow as BaseMarshmallow
from flask_marshmallow import sqla
from marshmallow import EXCLUDE


class SchemaOpts(sqla.SQLAlchemySchemaOpts):
    def __init__(self, meta, **kwargs):
        if not hasattr(meta, "unknown"):
            meta.Unknown = EXCLUDE
        super(SchemaOpts, self).__init__(meta, **kwargs)


class ModelSchema(sqla.SQLAlchemySchema):
    OPTIONS_CLASS = SchemaOpts


class Marshmallow(BaseMarshmallow):
    def __init__(self, app=None):
        super().__init__(app=app)
        self.ModelSchema = ModelSchema
