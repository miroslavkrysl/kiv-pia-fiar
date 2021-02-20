from dependency_injector import containers, providers
from flask import Flask

from fiar import cli
from fiar.di.providers.repositories import UserRepoProvider
from fiar.di.providers.services import HashServiceProvider, UidServiceProvider, UserServiceProvider, \
    AuthServiceProvider, TokenServiceProvider, PswdTokenServiceProvider, MailServiceProvider
from fiar.di.providers.sqlalchemy import SqlAlchemyDbProvider


class AppContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()

    app = providers.Dependency(instance_of=Flask)

    # --- DB ---
    sqlalchemy_db = providers.Resource(SqlAlchemyDbProvider, app)

    # --- Repos ---
    user_repo = providers.Resource(UserRepoProvider, app, sqlalchemy_db)

    #
    # friendship_repo = providers.Singleton(
    #     FriendshipRepo
    # )
    #
    # friendship_request_repo = providers.Singleton(
    #     FriendshipRequestRepo
    # )

    # --- Util services ---
    mail_service = providers.Resource(MailServiceProvider, app)
    hash_service = providers.Resource(HashServiceProvider, app)
    uid_service = providers.Resource(UidServiceProvider, app, user_repo)
    auth_service = providers.Resource(AuthServiceProvider, app, user_repo, hash_service)
    token_service = providers.Resource(TokenServiceProvider, app)
    pswd_token_service = providers.Resource(PswdTokenServiceProvider, token_service, user_repo)

    # --- Entity services ---
    user_service = providers.Resource(UserServiceProvider, app, user_repo, uid_service, hash_service)


def init_container(app: Flask):
    app.container = AppContainer(app=app)

    # wire all di dependencies
    app.container.wire(packages=[
        # routes
    ], modules=[
        cli
    ])
