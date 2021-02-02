from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from flask import Flask, request
from flask_socketio import SocketIO

from fiar.db import Db
from fiar.repositories.user import UserRepo
from fiar.services.auth import AuthService
from fiar.services.hash import HashService
from fiar.services.uid import UidService


class Container(containers.DeclarativeContainer):
    container_config = providers.Configuration()

    app = providers.Dependency(instance_of=Flask)

    db = providers.Resource(Db,
                            app)

    socket_io = providers.Singleton(
        SocketIO,
        app
    )

    request = providers.Resource(lambda: request)

    hash_service = providers.Singleton(
        HashService
    )

    uid_service = providers.Singleton(
        UidService,
        app.provided.config['UID']['LENGTH']
    )

    user_repo = providers.Singleton(
        UserRepo,
        hash_service,
        uid_service
    )

    auth_service = providers.Resource(
        AuthService,
        app,
        user_repo,
        hash_service
    )


def create_container(app: Flask):
    container = Container(app=app)
    app: Flask = container.app()

    # initialize db instance
    container.db.init()
    container.auth_service.init()

    app.before_first_request(before_first_request)
    app.before_request(before_request)
    app.teardown_appcontext(teardown_appcontext)

    return container


@inject
def before_first_request(container: Container = Provide[Container]):
    pass


@inject
def before_request(container: Container = Provide[Container]):
    # setup the request instance
    container.request.init()


@inject
def teardown_appcontext(exception):
    pass
