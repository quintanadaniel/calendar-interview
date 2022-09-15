from http import HTTPStatus

from apifairy import other_responses
from apifairy import response, arguments
from flask import Blueprint
from flask import jsonify
from flask import request
from sqlalchemy.orm import aliased

from application import db
from application.calendar.schemas import CalendarSchema
from application.models import User

calendar = Blueprint("calendar", __name__)
calendar_schema = CalendarSchema()
calendars_schema = CalendarSchema(many=True)


@calendar.route("/calendarinterviews", methods=["GET"])
def all_calendar_interviews():
    """Get all match between candidate and interviewer by param"""
    if (
        "candidate" not in request.args.keys()
        or "interviewers" not in request.args.keys()
    ):
        return (
            jsonify(
                error="the arguments should be one candidate and two interviewers split by coma"
            ),
            HTTPStatus.BAD_REQUEST,
        )
    if "," in request.args["candidate"]:
        return (
            jsonify(
                error="Maximum one candidate."
            ),
            HTTPStatus.BAD_REQUEST,
        )
    if len(request.args["interviewers"].split(",")) > 2:
        return (
            jsonify(
                error="Maximum two interviewers in the list."
            ),
            HTTPStatus.BAD_REQUEST,
        )

    params = request.args
    candidates_interviewers = []
    for candidate in (
        db.session.query(User)
        .filter(User.username == params["candidate"], User.role == "candidate")
        .all()
    ):

        interviewers = (
            db.session.query(User)
            .filter(
                User.username.in_(params["interviewers"].split(",")),
                User.role == "interviewer",
                User.available_date == candidate.available_date,
            )
            .all()
        )

        if len(interviewers) == 0:
            continue
        candidate_interviewers_json = {
            "candidate": calendar_schema.jsonify(candidate).json,
            "interviewers": calendars_schema.jsonify(interviewers).json,
        }
        candidates_interviewers.append(candidate_interviewers_json)
    if len(candidates_interviewers) == 0:
        return candidates_interviewers, HTTPStatus.NOT_FOUND
    return candidates_interviewers, HTTPStatus.OK
