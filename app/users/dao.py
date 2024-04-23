from app.dao.base import BaseDAO
from app.users.models import Users
from sqlalchemy import select
from app.database import async_session_market

class UsersDAO(BaseDAO):
    model = Users