from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from http import HTTPStatus
from jose import JWTError
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.utils.security import decode_access_token

# OAuth2 scheme - tells FastAPI where to look for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get current authenticated user from JWT token

    Args:
        token: JWT token from Authorization header
        session: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode token
        payload = decode_access_token(token)
        user_id: int = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Get user from database
    user = session.get(User, user_id)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user

    Args:
        current_user: Current user from get_current_user dependency

    Returns:
        Current active user

    Raises:
        HTTPException: If user is inactive
    """
    if current_user.status != 1:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Inactive user"
        )
    return current_user
