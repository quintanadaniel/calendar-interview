from marshmallow import fields

from application import ma


class CalendarSchema(ma.Schema):
    class Meta:
        fields = ("username", "role", "available_date")
