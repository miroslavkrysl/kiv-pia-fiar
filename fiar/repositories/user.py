from datetime import timedelta, datetime
from enum import Enum
from typing import Iterable

import pony.orm

from fiar.db import User


class UserRepo:
    class OrderBy(Enum):
        ID = User.id
        USERNAME = User.username
        EMAIL = User.email

    def __init__(self):
        pass

    def get_by_id(self, id: int) -> User:
        return User.get(id=id)

    def get_by_uid(self, uid: str) -> User:
        return User.get(uid=uid)

    def get_by_email(self, email: str):
        return User.get(email=email)

    def get_by_username(self, username: str):
        return User.get(username=username)

    def get_all(self, order_by: OrderBy = OrderBy.ID, desc=False) -> Iterable[User]:
        order = pony.orm.desc(order_by) if desc else order_by
        users = User.select().order_by(order)
        return users

    def get_all_online(self, max_inactive_time: timedelta) -> Iterable[User]:
        now = datetime.now()
        threshold = now - max_inactive_time
        return User.select(lambda p: p.last_active_at > threshold)

    def add(self, **kwargs) -> User:
        user = User(**kwargs)
        user.flush()

        return user
