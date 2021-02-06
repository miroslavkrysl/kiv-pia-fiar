from datetime import timedelta, datetime
from enum import Enum
from typing import Iterable

import pony.orm

from fiar.db import User
from fiar.services.hash import HashService
from fiar.services.uid import UidService


class UserRepo:
    class OrderBy(Enum):
        ID = User.id
        USERNAME = User.username
        EMAIL = User.email

    def __init__(self, hash_service: HashService, uid_service: UidService):
        self.hash_service = hash_service
        self.uid_service = uid_service

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

    def create(self,
               username: str,
               email: str,
               password: str,
               is_admin: bool = False,
               last_active_at: datetime = datetime.min) -> User:
        password = self.hash_service.hash(password)
        uid = self.uid_service.make_uid(self.get_by_uid)

        user = User(
            username=username,
            email=email,
            password=password,
            is_admin=is_admin,
            uid=uid,
            last_active_at=last_active_at)
        user.flush()

        return user
