from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class UsersTG(Base):
    __tablename__ = 'users_tg'

    id = Column(Integer, primary_key=True)
    id_tg = Column(String, unique=True)
    full_name = Column(String)
    access_bot = Column(Boolean, default=True)
