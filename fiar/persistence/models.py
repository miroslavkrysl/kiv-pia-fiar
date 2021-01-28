from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(int, primary_key=True, autoincrement=True)
    email = Column(String(254), unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_online = Column(Boolean, default=False, nullable=False)

    # for login/logout purposes
    # not stable value, can be changed over time
    uid = Column(String(64), default=False, nullable=False, unique=True)

