from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users_tg.schemas import SUsersTG, SUsersTg_FullData
from app.users_tg.dao import UsersTgDAO

router = APIRouter(prefix='/users-tg', tags=['Пользователи Telegram Bot'])


@router.get('')
async def get_users_tg(user_access: Users = Depends(get_current_user)) -> list[SUsersTg_FullData]:
    """Список пользователей (телеграм)"""
    users_tg = await UsersTgDAO.find_all()
    return users_tg

@router.post('')
# Annotated[SUsersTG, Depends()]
async def create_user_tg(user_data: SUsersTg_FullData, user_access: Users = Depends(get_current_user)) -> SUsersTg_FullData:
    """Добавить пользователя (телеграм)"""
    print('user_data', user_data)
    existing_user_tg = await UsersTgDAO.find_one_or_none(id_tg=user_data.id_tg)
    print('post', existing_user_tg)
    if existing_user_tg:
        raise HTTPException(
            status_code=409, detail="Пользователь телеграма уже существует")
    new_user_tg = await UsersTgDAO.add(
        id_tg=user_data.id_tg,
        full_name=user_data.full_name,
        access_bot=user_data.access_bot
    )
    return new_user_tg

@router.get('/{id_tg}')
async def get_user_item_tg(id_tg: str, user_access: Users = Depends(get_current_user)) -> SUsersTg_FullData:
    """Получить пользователя (телеграм)"""
    user = await UsersTgDAO.find_one_or_none(id_tg=id_tg)
    if not user:
        raise HTTPException(
            status_code=409, detail= "Пользователь телеграма отсутствует")
    return user


@router.put('/{id_tg}')
async def update_user_tg(id_tg: str, user_data: SUsersTG, user_access: Users = Depends(get_current_user)) -> SUsersTg_FullData:
    """Обновить пользователя (телеграм)"""
    existing_user_tg = await UsersTgDAO.find_one_or_none(id_tg=id_tg)
    if not existing_user_tg:
        raise HTTPException(
            status_code=404, detail='Пользователь телеграма отсутствует')
    update_user: SUsersTg_FullData = await UsersTgDAO.update_dao(id_tg, full_name=user_data.full_name, access_bot=user_data.access_bot)
    return update_user


@router.delete('/{id_tg}')
async def delete_user_tg(id_tg: str, user_access: Users = Depends(get_current_user)) -> bool:
    """Удалить пользователя (телеграм)"""
    existing_user_tg = await UsersTgDAO.find_one_or_none(id_tg=id_tg)
    if not existing_user_tg:
        raise HTTPException(
            status_code=404, detail="Пользователь телеграма отсутствует")
    await UsersTgDAO.delete(id_tg=id_tg)
    return True
