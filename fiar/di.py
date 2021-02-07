from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from flask import Flask, request
from flask_socketio import SocketIO

from fiar.db import Db
from fiar.repositories.user import UserRepo
from fiar.services.auth import AuthService
from fiar.services.hash import HashService
from fiar.services.mail import MailService
from fiar.services.pswd_reset import PswdResetService
from fiar.services.token import TokenService
from fiar.services.uid import UidService
from fiar.services.user import UserService


class Container(containers.DeclarativeContainer):
    container_config = providers.Configuration()

    app = providers.Dependency(instance_of=Flask)

    db = providers.Resource(Db,
                            app)

    socket_io = providers.Singleton(
        SocketIO,
        app
    )

    mail_service = providers.Singleton(
        MailService,
        app.provided.config['MAIL']['HOST'],
        app.provided.config['MAIL']['PORT'],
        app.provided.config['MAIL']['USER'],
        app.provided.config['MAIL']['PASSWORD'],
        app.provided.config['MAIL']['SSL'],
        app.provided.config['MAIL']['TLS'],
        app.provided.config['MAIL']['FROM_NAME'],
        app.provided.config['MAIL']['FROM_ADDR'],
    )

    user_repo = providers.Singleton(
        UserRepo
    )

    hash_service = providers.Singleton(
        HashService
    )

    uid_service = providers.Singleton(
        UidService,
        user_repo,
        app.provided.config['USER']['UID_LENGTH']
    )

    auth_service = providers.Resource(
        AuthService,
        app,
        user_repo,
        hash_service
    )

    token_service = providers.Resource(
        TokenService,
        app.provided.config['SECRET_KEY']
    )

    pswd_reset_service = providers.Resource(
        PswdResetService,
        token_service,
        user_repo,
        app.provided.config['USER']['PSWD_RESET_EXP']
    )

    user_service = providers.Singleton(
        UserService,
        user_repo,
        uid_service,
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
    pass


@inject
def teardown_appcontext(exception):
    pass
