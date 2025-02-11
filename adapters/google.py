import enum
from typing import Optional, Dict, Any

from adapters.base import OAuth2Adapter


class AccessType(enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class GoogleOAuth2Adapter(OAuth2Adapter):
    authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url = "https://oauth2.googleapis.com/token"

    def __init__(
        self,
        client_secret: str,
        access_type: Optional[AccessType] = AccessType.OFFLINE,
        *args,
        **kwargs,
    ):
        self.client_secret = client_secret
        self.access_type = access_type.value

        super(GoogleOAuth2Adapter, self).__init__(response_type="code", *args, **kwargs)

    def redirect_url_extra_params(self) -> Dict[str, Any]:
        return {
            "access_type": self.access_type,
        }

    def fetch_access_token_params(self) -> Dict[str, Any]:
        return {
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
        }

    def fetch_refresh_token_params(self) -> Dict[str, Any]:
        return {
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
        }
