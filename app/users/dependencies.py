from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from app.config import settings
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get(settings.TP_APP_ACCESS_TOKEN)
    if not token:
        raise HTTPException(status_code=401, detail='1. Токен отсутствует')
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=settings.ALGORITHM_JWT)
    except JWTError:
        #return None
        raise HTTPException(status_code=401, detail='2. Токен не является JWT')
    
    expire = payload.get('exp')
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=401, detail='3. Токен истек')
    
    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail='4. В токене нет данных о пользователе')
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail='5. Пользователь не найден')
    
    return  user       

""" async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
     if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user """