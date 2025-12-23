from pydantic import BaseModel, EmailStr


class Registration(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str
