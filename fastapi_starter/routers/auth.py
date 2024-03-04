"""Authentication Router."""

from fastapi import APIRouter, Depends, status

from ..controllers import auth as controller
from ..schemas.users import User, UserPublic

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
def get_current_user(current_user: User = Depends(controller.get_current_user)) -> User:
    """Returns the currently authenticated user."""
    return current_user
