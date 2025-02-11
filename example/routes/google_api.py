from flask import Blueprint, jsonify, request
from requests import HTTPError

from example.services.google import get_personal_information

google = Blueprint("google", __name__, url_prefix="/google")


@google.route("/me", methods=["GET"])
def login():
    user_id = request.args.get("user_id", type=int)

    try:
        personal_information = get_personal_information(user_id)
    except HTTPError as error:
        return jsonify({"error": error.response}), error.response.status_code

    return jsonify(**personal_information), 200
