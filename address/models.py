from sqlalchemy import  Column,  Integer, String
from .database import Base


class address(Base):

    __tablename__= "Addresses"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    longitude = Column(String, index=True)
    latitude = Column(String, index=True)

