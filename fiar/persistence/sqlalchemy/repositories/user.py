from collections import Iterable
from datetime import datetime, timedelta
from enum import Enum

from fiar.data.models import User
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.persistence.sqlalchemy.orm import user_table


class UserRepo:
    class OrderBy(Enum):
        ID = user_table.c.id
        USERNAME = user_table.c.username
        EMAIL = user_table.c.email
        LAST_ACTIVE_AT = user_table.c.last_active_at

    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_by_id(self, id: int) -> User:
        session = self.db.session
        return session.query(User).filter_by(id=id).first()

    def get_by_uid(self, uid: str) -> User:
        session = self.db.session
        return session.query(User).filter_by(uid=uid).first()

    def get_by_email(self, email: str):
        session = self.db.session
        return session.query(User).filter_by(email=email).first()

    def get_by_username(self, username: str):
        session = self.db.session
        return session.query(User).filter_by(username=username).first()

    def get_all(self, order_by: OrderBy = OrderBy.USERNAME) -> Iterable[User]:
        """
        Get all users.
        :param order_by: Order criterion.
        :return: Iterator of all users.
        """
        session = self.db.session
        users = session.query(User).order_by(order_by.value)
        return users

    def get_all_online(self, max_inactive_time: timedelta, order_by: OrderBy = OrderBy.USERNAME) -> Iterable[User]:
        """
        Get all online users.
        :param max_inactive_time: Maximum time from a moment when a user was last active.
        :param order_by: Order criterion.
        :return: Iterator of all online users.
        """
        now = datetime.now()
        threshold = now - max_inactive_time
        session = self.db.session
        users = session.query(User).filter(user_table.c.last_active_at >= threshold).order_by(order_by.value)
        return users

    def add(self, user: User):
        session = self.db.session
        session.add(user)
        session.commit()

    def delete(self, user: User):
        session = self.db.session
        session.delete(user)
        session.commit()
