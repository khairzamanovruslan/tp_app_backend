from sqlalchemy import Column, Integer, String
from app.database import Base


class Substation(Base):
    __tablename__ = 'substation'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    latitude = Column(String)
    longitude = Column(String)