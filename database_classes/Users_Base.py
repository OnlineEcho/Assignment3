from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


# get base class for table description
Base = declarative_base()  # returns a class to be used to create objects


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    secret_key = Column(String)
