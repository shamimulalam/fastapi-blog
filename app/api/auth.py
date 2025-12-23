from fastapi import APIRouter, Depends, HTTPException, Body
from http import HTTPStatus

from sqlmodel import Session, select

from app.schemas.auth.registration import Registration
from app.models.user import User
from app.database import get_session
from app.utils.security import hash_password

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
