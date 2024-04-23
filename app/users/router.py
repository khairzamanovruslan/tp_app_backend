from fastapi import APIRouter, HTTPException, Response
from app.users.auth import authenticate_user, get_password_hash, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth
from app.config import settings

router = APIRouter(prefix='/auth', tags=['Auth & Пользователи'])

@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    """Войти"""
    user = await authenticate_user(user_data.email, user_data.password)
    print('user', user)
    if not user:
        raise HTTPException(status_code=401, detail='Неверная почта или пароль') 
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(settings.TP_APP_ACCESS_TOKEN, access_token, httponly=True)
    return {"access_token": access_token}


@router.post('/logout')
async def logout_user(response: Response) -> bool:
    """Выйти"""
    response.delete_cookie(settings.TP_APP_ACCESS_TOKEN)
    return True


@router.post('/register')
async def register_users(register_key: str, user_data: SUserAuth) -> bool:
    """Регистрация"""
    print('register_key', user_data)
    if not settings.REGISTER_KEY == register_key:
        raise HTTPException(status_code=404, detail='Сорян, ошибочка вышла!')
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail='Пользователь существует')
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return True