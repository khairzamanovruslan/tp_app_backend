from app.dao.base import BaseDAO
from app.users_tg.models import UsersTG
from sqlalchemy import update, select
from app.database import async_session_market


class UsersTgDAO(BaseDAO):
    model = UsersTG

    @classmethod
    async def update_dao(cls, id_tg, **data):
        async with async_session_market() as session:
            query = (
                update(cls.model)
                .values(**data)
                .filter_by(id_tg=id_tg)
            ).returning(cls.model)
            update_user = await session.execute(query)
            await session.commit()
            return update_user.scalar_one_or_none()
