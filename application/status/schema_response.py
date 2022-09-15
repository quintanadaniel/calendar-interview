from marshmallow import fields

from application import ma


class StatusResponseSchema(ma.Schema):
    status = fields.String(dump_default="OK")
