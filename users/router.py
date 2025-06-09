from fastapi import APIRouter, HTTPException, Response, Depends

from users.auth import get_password_hash, create_access_token, authenticate_user
from users.dao import UsersDAO
from users.dependencies import get_current_user
from users.shemas import SUserAuth, SUserLogin

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
@router.post("/registration")
async def registration(user: SUserAuth, response: Response):
    check_user = await UsersDAO.find_one_or_none(email=user.email)
    if check_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)

    await UsersDAO.create(email=user.email, hashed_password=hashed_password)
    user = await UsersDAO.find_one_or_none(email=user.email)
    user_id = user['id']
    access_token = create_access_token({"sub": int(user_id)})
    response.set_cookie("token", value=access_token, httponly=True)

@router.post("/login")
async def login(suser: SUserLogin, response: Response):
    user = await authenticate_user(suser.email, suser.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": int(user["id"])})
    response.set_cookie("token", value=access_token, httponly=True)
    return {"user": user}

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("token")

@router.post("/delete_account")
async def delete_account(response: Response, user = Depends(get_current_user)):
    response.delete_cookie("token")

    return await UsersDAO.delete_user(user.id)
