from flask import Flask

from fiar.data.repositories.friendship import FriendshipRepo
from fiar.data.repositories.friendship_request import FriendshipRequestRepo
from fiar.data.repositories.user import UserRepo
from fiar.di.providers import ServiceProvider
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb


class UserRepoProvider(ServiceProvider):

    def init(self, app: Flask, db: SqlAlchemyDb) -> UserRepo:
        return UserRepo(db)

    def shutdown(self, resource: UserRepo) -> None:
        pass


class FriendshipRepoProvider(ServiceProvider):

    def init(self, app: Flask, db: SqlAlchemyDb) -> FriendshipRepo:
        return FriendshipRepo(db)

    def shutdown(self, resource: FriendshipRepo) -> None:
        pass


class FriendshipRequestRepoProvider(ServiceProvider):

    def init(self, app: Flask, db: SqlAlchemyDb) -> FriendshipRequestRepo:
        return FriendshipRequestRepo(db)

    def shutdown(self, resource: FriendshipRequestRepo) -> None:
        pass
