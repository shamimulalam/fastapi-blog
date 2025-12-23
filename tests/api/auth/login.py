from http import HTTPStatus

from app.models.user import User
from app.utils.security import hash_password


def test_successful_login(client, session):
    #create user
    example_user = {
        "first_name": "Karim",
        "last_name": "Khan"
    }
    payload = {
        "email": "karim@khan.com",
        "password": "password"
    }

    user_model = User(
        first_name=example_user["first_name"],
        last_name=example_user["last_name"],
        email=payload["email"],
        password=hash_password(payload["password"])
    )

    session.add(user_model)
    session.commit()
    #login request
    response = client.post("/login",  json=payload)
    #assert successful attempt
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "access_token" in data
    assert response.headers["content-type"] == "application/json"
    assert "content-length" in response.headers
    assert data["token_type"] == "bearer"


def test_invalid_email(client, session):
    #create user
    example_user = {
        "first_name": "Karim",
        "last_name": "Khan",
        "email": "karin@khan.xyz",
        "password": "password@1243",
    }
    payload = {
        "email": "karim@khan.com",
        "password": "password"
    }

    user_model = User(
        first_name=example_user["first_name"],
        last_name=example_user["last_name"],
        email=example_user["email"],
        password=hash_password(payload["password"])
    )

    session.add(user_model)
    session.commit()
    #login request
    response = client.post("/login",  json=payload)
    #assert successful attempt
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Invalid Email or Password"

def test_invalid_password(client, session):
    #create user
    example_user = {
        "first_name": "Karim",
        "last_name": "Khan",
        "email": "karin@khan.xyz",
        "password": "password@1243",
    }
    payload = {
        "email": "karim@khan.com",
        "password": "password"
    }

    user_model = User(
        first_name=example_user["first_name"],
        last_name=example_user["last_name"],
        email=payload["email"],
        password=hash_password(example_user["password"])
    )

    session.add(user_model)
    session.commit()
    #login request
    response = client.post("/login",  json=payload)
    #assert successful attempt
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json()["detail"] == "Invalid Email or Password"
