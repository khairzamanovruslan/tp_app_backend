from fastapi import APIRouter, Depends, HTTPException
from app.substation.dao import SubstationDAO
from app.substation.schemas import SSubstation_Coordinates, SSubstation_NameCoordinates, SSubstation_FullData
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix='/substation', tags=['ТП'])


@router.post('')
async def create_substation(
    substation_data: SSubstation_NameCoordinates, 
    user_access: Users = Depends(get_current_user)
    ) -> SSubstation_NameCoordinates:
    """Создать ТП"""
    existing_substation = await SubstationDAO.find_one_or_none(name=substation_data.name)
    if existing_substation:
        raise HTTPException(
            status_code=409, detail="Такая ТП уже существует")
    new_substation = await SubstationDAO.add(
        name=substation_data.name,
        latitude=substation_data.latitude,
        longitude=substation_data.longitude
    )
    return new_substation


@router.get('')
async def get_substations(user_access: Users = Depends(get_current_user)) -> list[SSubstation_FullData]:
    """Список ТП"""
    print('get_substations', user_access)
    substations_data = await SubstationDAO.find_all()
    list_substation = []
    for item in substations_data:
        item = dict(item)
        link = {"link": f'https://yandex.ru/maps/?pt={item['longitude']},{item['latitude']}&z=18&l=map'}
        item.update(link)
        list_substation.append(item)
    return list_substation


@router.get('/{name}')
async def get_substation(name: str, user_access: Users = Depends(get_current_user))-> SSubstation_FullData:
    """Получить ТП"""
    substation_data: SSubstation_FullData = await SubstationDAO.find_one_or_noneDAO(name=name)
    if not substation_data:
        raise HTTPException(
            status_code=409, detail= "Такая ТП отсутствует")
    substation = dict(substation_data)
    link = {"link": f'https://yandex.ru/maps/?pt={substation['longitude']},{substation['latitude']}&z=18&l=map'}
    substation.update(link)
    return substation


@router.put('/{name}')
async def update_substation(
    name: str, 
    substation_data: SSubstation_Coordinates, 
    user_access: Users = Depends(get_current_user)) -> bool:
    """Обновить ТП"""
    existing_substation = await SubstationDAO.find_one_or_none(name=name)
    if not existing_substation:
        raise HTTPException(
            status_code=404, detail="Такая ТП отсутствует")
    update_substation = await SubstationDAO.update_dao(
        name, 
        latitude=substation_data.latitude, 
        longitude=substation_data.longitude)
    print('put', update_substation)
    return True


@router.delete('/{name}')
async def delete_substation(name: str, user_access: Users = Depends(get_current_user)) -> bool:
    """Удалить ТП"""
    existing_substation = await SubstationDAO.find_one_or_none(name=name)
    if not existing_substation:
        raise HTTPException(
            status_code=404, detail="Такая ТП отсутствует")
    await SubstationDAO.delete(name=name)
    return True
