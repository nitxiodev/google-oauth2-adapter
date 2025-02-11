import time

from example.extensions import db
from example.models import SocialToken
from utils import TokenStore


def create_social_token(user_id: int, token_data: TokenStore):
    social_token = SocialToken(
        access_token=token_data.access_token,
        refresh_token=token_data.refresh_token,
        expires_at=time.time() + token_data.expires_in,
        user_id=user_id,
    )
    db.session.add(social_token)
    db.session.commit()

    return social_token
