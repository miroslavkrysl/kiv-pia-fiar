from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(String(32), primary_key=True)
