from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Customer(Base, SerializerMixin):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)

class TranslationSource(Base, SerializerMixin):
    __tablename__ = "translation_source"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String)
    source_url = Column(String)
    query_format = Column(String)

class Translation(Base, SerializerMixin):
    __tablename__ = "translation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=True)
    id_source = Column(Integer, ForeignKey(TranslationSource.id), nullable=False)