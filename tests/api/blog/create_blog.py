from http import HTTPStatus

from sqlmodel import select

from app.models.blog import Blog


def test_create_blog(client, session):
    #create new blog
    payload = {
        "title": "This is title",
        "post": "Hello this is post",
    }

    response = client.post("/blog/", json=payload)

    query = select(Blog)
    db_blog = session.exec(query).first()

    #assert blog created
    assert response.status_code == HTTPStatus.CREATED
    assert db_blog is not None
    assert db_blog.title == payload["title"]
    assert db_blog.post == payload["post"]

def test_empty_title(client, session):
    #create new blog
    payload = {
        "post": "Hello this is post",
    }

    response = client.post("/blog/", json=payload)

    #assert blog created
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT