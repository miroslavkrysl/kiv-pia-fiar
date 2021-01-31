import sys

from dependency_injector import containers, providers
from flask import Flask, request
from flask_socketio import SocketIO

from fiar.persistence.db import initialize_db
from fiar.persistence.repositories import UserRepository


# class DatabaseModule(Module):
#     @singleton
#     @provider
#     def provide(self, app: Flask) -> Database:
#         return Database(app)
#
#
# class HashModule(Module):
#     @singleton
#     @provider
#     def provide(self) -> HashService:
#         return HashService()
#
#
# class TokenModule(Module):
#     @singleton
#     @provider
#     def provide(self, app: Flask) -> TokenService:
#         return TokenService(app.config['SECRET_KEY'], app.config['APP_TOKEN_EXP'])
#
#
# class SocketIoModule(Module):
#
#     @singleton
#     @provider
#     def provide(self, app: Flask) -> SocketIO:
#         socket_io = SocketIO(app)
#         return socket_io
#
#
# # class MailService(Module):
# #
# #     @singleton
# #     @provider
# #     def provide(self, mail: Mail) -> MailService:
# #         mail_service = MailService(mail)
# #         return mail_service
#
#
# # --- Repositories ---
#
# class MailModule(Module):
#
#     @singleton
#     @provider
#     def provide(self, app: Flask) -> Mail:
#         mail = Mail(app)
#         return mail
#
#
# class UserRepositoryModule(Module):
#
#     @singleton
#     @provider
#     def provide(self, database: Database) -> UserRepository:
#         repository = UserRepository(database)
#         return repository
#
#
# modules = [
#     DatabaseModule,
#     TokenModule,
#     UserRepositoryModule,
#     SocketIoModule,
#     HashModule,
#     MailModule
# ]
#
#
# def initialize_di(app: Flask) -> FlaskInjector:
#     di = FlaskInjector(app=app, modules=modules)
#
#     # Force instantiation of singletons on application startup.
#     # If not done, it causes errors, because some setup logic
#     # may be called after first request, which is late.
#     di.injector.get(Database)
#
#     return di


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    app = providers.Dependency(instance_of=Flask)
    database = providers.Resource(initialize_db, app)

    # --- websockets - Socket.IO ---
    socket_io = providers.Singleton(
        SocketIO,
        app
    )

    # --- Request ---
    request = providers.Resource(lambda: request)

    # --- Repositories ---
    user_repository = providers.Singleton(
        UserRepository,
        database,
    )


def create_container(app: Flask):
    container = Container(app=app)

    @app.before_first_request
    def init_app_resources():
        container.database.init()

    @app.before_request
    def init_request_resources():
        container.request.init()

    @app.teardown_request
    def shutdown_request_resources(self):
        pass

    return container
