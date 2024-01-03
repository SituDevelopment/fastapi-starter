"""Users Controller."""


from uuid import UUID

from sqlalchemy.orm import Session

from ..models.users import *
from ..schemas import EmailStr
from ..schemas.users import *


def create_user(session: Session, item: UserCreate) -> User:
    """Creates the given user."""
    user = UserModel(**item.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return User(**user.as_dict())


def delete_user(session: Session, id: UUID) -> None:
    """Deletes the user specified by the given ID."""
    session.delete(get_user(session, id))
    session.commit()


def get_user(session: Session, id: UUID) -> User:
    """Returns the user specified by the given ID."""
    return User(**session.query(UserModel).filter_by(id=id).one().as_dict())


def get_user_by_username(session: Session, username: EmailStr) -> User:
    """Returns the user specified by the given username."""
    return User(**session.query(UserModel).filter_by(username=username).one().as_dict())


def get_users(session: Session) -> list[User]:
    """Returns all users."""
    return [User(**user.as_dict()) for user in session.query(UserModel).all()]


def update_user(session: Session, id: UUID, item: UserUpdate) -> User:
    """Updates the user specified by the given ID."""
    session.query(UserModel).filter_by(id=id).update(
        item.model_dump(exclude_unset=True)
    )
    session.commit()
    return get_user(session, id)
