from flask import Blueprint, request, jsonify

from example.services.google import get_personal_information

google = Blueprint("google", __name__, url_prefix="/google")


@google.route("/me", methods=["GET"])
def login():
    user_id = request.args.get("user_id", type=int)
    personal_information = get_personal_information(user_id)

    return jsonify(**personal_information), 200
