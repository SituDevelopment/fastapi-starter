"""Grants administrators permissions to resources."""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..controllers.organisations import get_organisation
from ..schemas.organisations import PermissionType
from ..schemas.users import User
from .database import database


class Admin:
    """
    Requires the user to be a member of an organisation with administrative permissions.
    """

    def __call__(self, user: User, session: Session = Depends(database)) -> User:
        organisation = get_organisation(session, user.organisation)

        if organisation.permission == PermissionType.ADMIN:
            return user

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
