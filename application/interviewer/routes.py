from http import HTTPStatus

from apifairy import body
from apifairy import response
from flask import Blueprint
from flask import jsonify

from application import db
from application.interviewer.schemas import InterviewerSchema
from application.models import User

interviewer = Blueprint("interviewer", __name__)
interviewer_schema = InterviewerSchema()
interviewers_schema = InterviewerSchema(many=True)


@interviewer.route("/interviewers", methods=["POST"])
@body(interviewer_schema)
@response(interviewer_schema, 201)
def create(args):
    """Register a new user"""
    role = "interviewer"
    args["role"] = role
    user_exists = (
        db.session.query(User)
        .filter_by(
            username=args["username"], role=role, available_date=args["available_date"]
        )
        .count()
    )
    if user_exists > 0:
        return jsonify(message="interviewer exists"), HTTPStatus.BAD_REQUEST
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    return user


@interviewer.route("/interviewers", methods=["GET"])
@response(interviewers_schema)
def all():
    """Retrieve all interviewers"""
    users = db.session.query(User).filter_by(role="interviewer").all()
    if len(users) > 0:
        return users
    return users, HTTPStatus.NOT_FOUND
