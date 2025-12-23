from pydantic import BaseModel

class Registration(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str