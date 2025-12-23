from fastapi import APIRouter, Depends, HTTPException, Body
from http import HTTPStatus
from datetime import timedelta

from sqlmodel import Session, select

from app.schemas.auth.login import Login
from app.schemas.auth.registration import Registration
from app.models.user import User
from app.database import get_session
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
router = APIRouter()


@router.post("/register", tags=["Authentication"], status_code=HTTPStatus.CREATED)
async def user_registration(
        payload: Registration = Body(
            ...,
            openapi_examples={
                "normal": {
                    "summary": "Normal Registration",
                    "description": "A typical user registration",
                    "value": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@example.com",
                        "password": "SecurePass123!",
                        "confirm_password": "SecurePass123!"
                    }
                },
                "another_user": {
                    "summary": "Another User",
                    "description": "Registration with different data",
                    "value": {
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "email": "jane.smith@company.com",
                        "password": "MyP@ssw0rd123",
                        "confirm_password": "MyP@ssw0rd123"
                    }
                }
            }
        ),
        session: Session = Depends(get_session)
):
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Passwords do not match"
        )

    statement = select(User).where(User.email == payload.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(payload.password)

    new_user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "message": "user registered",
        "user": {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "status": new_user.status
        }
    }

@router.post("/login", tags=["Authentication"], status_code=HTTPStatus.OK)
async def user_login(
    payload: Login = Body(
            ...,
            openapi_examples={
                "normal": {
                    "summary": "First User Login",
                    "description": "A typical user registration",
                    "value": {
                        "email": "john.doe@example.com",
                        "password": "SecurePass123!"
                    }
                },
                "another_user": {
                    "summary": "Second User Login",
                    "description": "Registrated with different data",
                    "value": {
                        "email": "jane.smith@company.com",
                        "password": "MyP@ssw0rd123"
                    }
                }
            }
        ),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.email == payload.email)).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid Email or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid Email or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.status != 1:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Inactive user account",
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }



