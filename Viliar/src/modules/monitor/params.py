from marshmallow import Schema, fields


class MonitorServerSchema(Schema):
    entity = fields.String(required=True)
