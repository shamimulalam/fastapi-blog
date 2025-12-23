from http import HTTPStatus

from sqlalchemy.sql.functions import user
from sqlmodel import select
from app.models.user import User
from app.utils.security import verify_password, hash_password


def test_registration(client, session):
    """Test user registration and verify database entry"""
    payload = {
        "first_name": "Karim",
        "last_name": "Khan",
        "email": "karim@khan.com",
        "password": "password",
        "confirm_password": "password",
    }

    # Make registration request
    response = client.post("/register", json=payload)

    # Assert response
    assert response.status_code == HTTPStatus.CREATED
    # assert response.json() == {"message": "user registered"}

    # Fetch user from database
    statement = select(User).where(User.email == "karim@khan.com")
    user = session.exec(statement).first()

    # Verify user exists in database
    assert user is not None, "User should be saved in database"
    assert user.first_name == payload["first_name"]
    assert user.last_name == payload["last_name"]
    assert user.email == payload["email"]
    assert user.status == 1
    assert user.id == 1

    # Verify password is hashed (not plain text)
    assert verify_password(payload["password"], user.password) is True
    assert user.password != "password", "Password should be hashed"
    assert user.password is not None, "Password should be stored"


def test_unique_registration(client, session):
    """Test user registration and verify database entry"""
    payload = {
        "first_name": "Karim",
        "last_name": "Khan",
        "email": "karim@khan.com",
        "password": "password",
        "confirm_password": "password",
    }

    old_user = User(
        first_name= payload["first_name"],
        last_name= payload["last_name"],
        email= payload["email"],
        password=hash_password(payload["password"])
    )

    session.add(old_user)
    session.commit()

    response = client.post("/register", json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json().get("detail") == "Email already registered"
