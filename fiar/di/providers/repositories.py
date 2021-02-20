from flask import Flask

from fiar.data.repositories.user import UserRepo
from fiar.di.providers import ServiceProvider
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb


class UserRepoProvider(ServiceProvider):

    def init(self, app: Flask, db: SqlAlchemyDb) -> UserRepo:
        return UserRepo(db)

    def shutdown(self, resource: UserRepo) -> None:
        pass
