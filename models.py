from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Customer(Base, SerializerMixin):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
