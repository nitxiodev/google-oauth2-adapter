from dataclasses import dataclass
from random import SystemRandom
from typing import Optional

from oauthlib.common import UNICODE_ASCII_CHARACTER_SET


@dataclass
class TokenStore:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = 0


def generate_random_state(length=30) -> str:
    """Taken from requests-oauthlib package"""
    rand = SystemRandom()
    return "".join(rand.choice(UNICODE_ASCII_CHARACTER_SET) for _ in range(length))
