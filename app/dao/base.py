from sqlalchemy import select, insert, delete
from app.database import async_session_market


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_market() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_market() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            new_data = await session.execute(query)
            await session.commit()
            return new_data.scalar()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_market() as session:
            query = select(cls.model).filter_by(**filter_by)# .__table__.columns
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_market() as session:
            query = delete(cls.model).filter_by(
                **filter_by)
            result = await session.execute(query)
            await session.commit()
            return result


    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_market() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()