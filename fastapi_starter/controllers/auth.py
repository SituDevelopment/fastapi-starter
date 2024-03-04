"""Authentication Controller."""

from os import environ

from fastapi import BackgroundTasks, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import Fief, FiefAccessTokenInfo
from fief_client.integrations.fastapi import FiefAuth
from sqlalchemy.orm import Session

from ..dependencies.database import database
from ..schemas.users import User
from .users import get_user

FIEF_BASE_URL = environ["FIEF_BASE_URL"]
CLIENT_ID = environ["CLIENT_ID"]
CLIENT_SECRET = environ["CLIENT_SECRET"]

FIEF_CLIENT = Fief(FIEF_BASE_URL, CLIENT_ID, CLIENT_SECRET)

OAUTH2_SCHEME = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{FIEF_BASE_URL}/authorize",
    tokenUrl=f"{FIEF_BASE_URL}/api/token",
    scopes={"openid": "openid", "offline_access": "offline_access"},
    auto_error=False,
)
"""The OAuth2 scheme used to authenticate users."""

IDENTITY_PROVIDER = FiefAuth(FIEF_CLIENT, OAUTH2_SCHEME)
"""Integration with the identity provider."""


BACKGROUND_TASKS = BackgroundTasks()
"""Background tasks."""


async def get_current_user(
    session: Session = Depends(database),
    access_token_info: FiefAccessTokenInfo = Depends(IDENTITY_PROVIDER.authenticated()),
) -> User:
    """
    Returns the current user.

    Returns
    -------
        `User`: the current user
    """
    return get_user(session, access_token_info["id"])
