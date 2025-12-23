from http import HTTPStatus

from fastapi import APIRouter, Depends, Body
from sqlmodel import Session

from app.database import get_session
from app.schemas.blog.blog import BlogBase
from app.models.blog import Blog

router = APIRouter()

@router.post("/blog", tags=["Blog"], status_code=HTTPStatus.CREATED)
async def create_blog(
        payload: BlogBase = Body(
            ...,
            openapi_examples={
                "normal": {
                    "summary": "A normal blog post",
                    "description": "A typical blog post with title and content",
                    "value": {
                        "title": "Getting Started with FastAPI",
                        "post": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+..."
                    }
                },
                "short": {
                    "summary": "A short blog post",
                    "description": "A minimal blog post example",
                    "value": {
                        "title": "Quick Update",
                        "post": "Just a quick update on the project status."
                    }
                },
                "technical": {
                    "summary": "A technical blog post",
                    "description": "A blog post with technical content",
                    "value": {
                        "title": "Understanding SQLModel Foreign Keys",
                        "post": "When defining foreign keys in SQLModel, always use lowercase table names like 'user.id' instead of 'User.id'..."
                    }
                }
            }
        ),
        session: Session = Depends(get_session)
) -> Blog:
    blog = Blog(
        user_id=1,
        title=payload.title,
        post=payload.post,
    )
    session.add(blog)
    session.commit()
    session.refresh(blog)

    return blog