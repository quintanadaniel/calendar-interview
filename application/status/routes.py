from http import HTTPStatus

from apifairy import response
from flask import Blueprint
from flask import jsonify

from application.status.schema_response import StatusResponseSchema

status_bp = Blueprint("status_bp", __name__)
status_response_schema = StatusResponseSchema()


@status_bp.route("/status")
@response(status_response_schema, HTTPStatus.OK, "available")
def status():
    """Available status API"""
    return jsonify(status="OK"), HTTPStatus.OK
