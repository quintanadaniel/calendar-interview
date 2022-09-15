from marshmallow import ValidationError
from marshmallow import fields
from marshmallow import validates

from application import ma
from application.models import User

"""
# ModelSchema
class CandidateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

        fields = ("username", "role", "available_date")

    username = ma.auto_field(required=True)
    role = ma.auto_field(required=False)
    available_date = ma.Datetime(required=True)

    @validates("available_date")
    def validate_available_date(self, value):
        if value.minute > 0:
            raise ValidationError("The range of time should be for hour.")
"""


# Schema, not valid with data base Model
class CandidateSchema(ma.Schema):
    username = fields.String()
    available_date = fields.DateTime("%Y-%m-%d %H:%M")

    @validates("available_date")
    def validate_available_date(self, value):
        if value.minute > 0:
            raise ValidationError("The range of time should be for hour.")

    class Meta:
        fields = ("username", "role", "available_date")
