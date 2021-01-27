from flask import Flask
from flask_injector import FlaskInjector
from flask_mail import Mail
from flask_socketio import SocketIO
from injector import Module, singleton, provider

from fiar.persistence.db import Database
from fiar.persistence.repositories import UserRepository
from fiar.services.security import HashService


class DbModule(Module):
    @singleton
    @provider
    def provide(self, app: Flask) -> Database:
        return Database(app)


class HashModule(Module):
    @singleton
    @provider
    def provide(self) -> HashService:
        return HashService()


class SocketIoModule(Module):

    @singleton
    @provider
    def provide(self, app: Flask) -> SocketIO:
        socket_io = SocketIO(app)
        return socket_io


# class MailService(Module):
#
#     @singleton
#     @provider
#     def provide(self, mail: Mail) -> MailService:
#         mail_service = MailService(mail)
#         return mail_service


# --- Repositories ---

class MailModule(Module):

    @singleton
    @provider
    def provide(self, app: Flask) -> Mail:
        mail = Mail(app)
        return mail


class UserRepositoryModule(Module):

    @singleton
    @provider
    def provide(self, database: Database) -> UserRepository:
        repository = UserRepository(database)
        return repository


modules = [
    DbModule,
    UserRepositoryModule,
    SocketIoModule,
    HashModule,
    MailModule
]


def initialize_di(app: Flask) -> FlaskInjector:
    di = FlaskInjector(app=app, modules=modules)

    # Force instantiation of singletons on application startup.
    # If not done, it causes errors, because some setup logic
    # may be called after first request, which is late.
    di.injector.get(Database)

    return di
