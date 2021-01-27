from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    username = Column(String(32), primary_key=True)
    # email = Column(String(254), unique=True, nullable=False)
    # password = Column(String(255), nullable=False)
    # is_admin = Column(Boolean, default=False, nullable=False)
    # is_online = Column(Boolean, default=False, nullable=False)
