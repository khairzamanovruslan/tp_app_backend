from app.dao.base import BaseDAO
from app.substation.models import Substation
from sqlalchemy import select, update
from app.database import async_session_market


class SubstationDAO(BaseDAO):
    model = Substation

    @classmethod
    async def find_one_or_noneDAO(cls, **filter_by):
        async with async_session_market() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            data = await session.execute(query)
            result = data.mappings().all()
            if not result:
                return None
            return result[0]
        
    @classmethod
    async def update_dao(cls, name, **data):
        async with async_session_market() as session:
            query = (
                update(cls.model)
                .values(**data)
                .filter_by(name=name)
            ).returning(cls.model)
            update_substation = await session.execute(query)
            await session.commit()
            return update_substation.scalar_one_or_none()