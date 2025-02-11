import requests
from werkzeug.exceptions import NotFound

from example.extensions import db
from example.models import SocialToken


def get_personal_information(user_id: int):
    social_token = db.session.execute(
        db.select(SocialToken).where(SocialToken.user_id == user_id)
    ).scalar()

    if not social_token:
        raise NotFound("Social token not found")

    requests_session = requests.Session()
    requests_session.headers.update(
        {
            "Authorization": f"Bearer {social_token.safe_access_token}",
        }
    )
    response = requests_session.get(
        "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    )
    response.raise_for_status()

    return response.json()
