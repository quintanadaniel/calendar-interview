import uuid
from http import HTTPStatus

from apifairy import body
from apifairy import response
from flask import Blueprint
from flask import jsonify

from application import db
from application.candidate.schemas import CandidateSchema
from application.models import User

candidate = Blueprint("candidate", __name__)
candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)


@candidate.route("/candidates", methods=["POST"])
@body(candidate_schema)
@response(candidate_schema, 201)
def create(args):
    """Register a new user"""
    role = "candidate"
    args["role"] = role
    user_exists = (
        db.session.query(User)
        .filter_by(
            username=args["username"], role=role, available_date=args["available_date"]
        )
        .count()
    )
    if user_exists > 0:
        return jsonify(message="candidate exists"), HTTPStatus.BAD_REQUEST
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    return user


@candidate.route("/candidates", methods=["GET"])
@response(candidates_schema)
def all():
    """Retrieve all users"""
    users = db.session.query(User).filter_by(role="candidate").all()
    if len(users) > 0:
        return users
    return users, HTTPStatus.NOT_FOUND
