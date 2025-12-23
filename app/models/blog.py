from sqlmodel import SQLModel, Field

class Blog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    title: str
    post: str | None = None