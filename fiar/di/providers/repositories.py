from flask import Flask

from fiar.persistence.sqlalchemy.repositories.friendship import FriendshipRepo
from fiar.persistence.sqlalchemy.repositories.game import GameRepo
from fiar.persistence.sqlalchemy.repositories.invite import InviteRepo
from fiar.persistence.sqlalchemy.repositories.request import RequestRepo
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
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


class RequestRepoProvider(ServiceProvider):

    def init(self, app: Flask, db: SqlAlchemyDb) -> RequestRepo:
        return RequestRepo(db)

    def shutdown(self, resource: RequestRepo) -> None:
        pass


class GameRepoProvider(ServiceProvider):

    def init(self, app: Flask, db: SqlAlchemyDb) -> GameRepo:
        return GameRepo(db)

    def shutdown(self, resource: GameRepo) -> None:
        pass


class InviteRepoProvider(ServiceProvider):

    def init(self, app: Flask, db: SqlAlchemyDb) -> InviteRepo:
        return InviteRepo(db)

    def shutdown(self, resource: InviteRepo) -> None:
        pass
