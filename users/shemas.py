from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    name: str
    password: str
    email: EmailStr

class SUserLogin(BaseModel):
    password: str
    email: EmailStr