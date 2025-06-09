from datetime import datetime

from fastapi import Request, HTTPException, Depends
from jose import jwt
from starlette import status

from users.dao import UsersDAO

def get_token(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        decoded_jwt = jwt.decode(
            token,
            key="WymgCrsTn2KuSCpv2XxY7e87MwC5SKzysyfexrsNR/c=",
            algorithms=["HS256"]
        )
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    expire: str = decoded_jwt.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Expired')
    user_id: str = decoded_jwt.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Found')
    user = await UsersDAO.find_one_or_none(id=int(user_id))

    return user