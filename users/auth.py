from passlib.context import CryptContext
from datetime import timedelta, datetime
from users.dao import UsersDAO
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, "WymgCrsTn2KuSCpv2XxY7e87MwC5SKzysyfexrsNR/c=", "HS256")
    return encoded_jwt

async def authenticate_user(email: str, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    hashed_password = user["hashed_password"]
    if not user or not verify_password(password, hashed_password):
        return None
    return user