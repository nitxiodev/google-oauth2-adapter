import urllib.parse
from typing import List, Any, Dict, Optional

import requests

from utils import generate_random_state, TokenStore


class OAuth2Error(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message, status_code)


class AdapterClient(requests.Session):
    def perform_request(self, method="POST", url=None, data=None):
        request = self.request(
            method=method,
            url=url,
            json=data,
        )
        request.raise_for_status()
        return request.json()


class OAuth2Adapter:
    authorization_url = None
    token_url = None
    client = AdapterClient()

    def __init__(
        self,
        client_id: str,
        redirect_uri: str,
        response_type: str,
        scope: List[str],
        state: Optional[str] = None,
        **kwargs,
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.scope = scope
        self.state = state

    def redirect_url_extra_params(self) -> Dict[str, Any]:
        raise NotImplementedError("Not implemented yet!")

    def fetch_access_token_params(self) -> Dict[str, Any]:
        raise NotImplementedError("Not implemented yet!")

    def fetch_refresh_token_params(self) -> Dict[str, Any]:
        raise NotImplementedError("Not implemented yet!")

    @property
    def redirect_url(self):
        self.state = self.state or generate_random_state()

        url_params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "scope": " ".join(self.scope),
            "state": self.state,
        }

        adapter_redirect_url_extra_params = self.redirect_url_extra_params()
        if adapter_redirect_url_extra_params:
            url_params.update(adapter_redirect_url_extra_params)

        urlencoded_string = urllib.parse.urlencode(url_params)
        return f"{self.authorization_url}?{urlencoded_string}", self.state

    def fetch_access_token(
        self, authorization_response_url: str, state=None
    ) -> TokenStore:
        parsed_url = urllib.parse.urlparse(authorization_response_url)
        url_params = dict(urllib.parse.parse_qsl(parsed_url.query))

        if "error" in url_params:
            error = url_params["error"]
            raise OAuth2Error(message=error, status_code=400)

        authorized_state = url_params.get("state")
        if authorized_state is not None and authorized_state != state:
            raise OAuth2Error(
                message="State mismatch between request and response", status_code=400
            )

        code = url_params.get("code")
        body = {
            "client_id": self.client_id,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }

        adapter_fetch_access_token_params = self.fetch_access_token_params()
        if adapter_fetch_access_token_params:
            body.update(adapter_fetch_access_token_params)

        response = self.client.perform_request(url=self.token_url, data=body)
        return TokenStore(
            access_token=response.get("access_token"),
            refresh_token=response.get("refresh_token"),
            expires_in=response.get("expires_in"),
        )

    def refresh_access_token(self, refresh_token: str) -> TokenStore:
        body = {"client_id": self.client_id, "refresh_token": refresh_token}

        adapter_fetch_refresh_token_params = self.fetch_refresh_token_params()
        if adapter_fetch_refresh_token_params:
            body.update(adapter_fetch_refresh_token_params)

        response = self.client.perform_request(url=self.token_url, data=body)
        return TokenStore(
            access_token=response.get("access_token"),
            expires_in=response.get("expires_in"),
        )
