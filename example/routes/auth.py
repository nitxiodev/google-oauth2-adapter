from flask import Blueprint, Response, current_app, redirect, request, session

from adapters.base import OAuth2Error
from example.services.social import create_social_token

auth = Blueprint("auth", __name__, url_prefix="/")


@auth.route("/", methods=["GET"])
def login():
    google_adapter = current_app.extensions["google_adapter"]
    redirect_url, state = google_adapter.redirect_url

    # Keep the state for later use
    session["state"] = state
    return redirect(redirect_url)


@auth.route("/callback", methods=["GET"])
def callback():
    try:
        google_adapter = current_app.extensions["google_adapter"]
        response = google_adapter.fetch_access_token(
            request.url, state=session["state"]
        )

        # In real applications, here we should make an API call to fetch the user email
        # or something what we can use to perform a lookup in the database and fetch the right user from it

        # 1 is the user id. It is hardcoded for example purposes only
        create_social_token(1, response)

        return Response("Login successful"), 200
    except OAuth2Error as error:
        return Response(error.message), error.status_code
