import uuid

from guid import guid
import sqlalchemy as sqla

from application import db


class User(db.Model):
    __tablename__ = "users"
    username = sqla.Column(sqla.String(), primary_key=True, nullable=False)
    role = sqla.Column(sqla.String(), primary_key=True, nullable=False)
    available_date = sqla.Column(sqla.DateTime(), primary_key=True)

    def __repr__(self):
        return "<User {} {} {}>".format(self.username, self.role, self.available_date)
