from dependency_injector import containers, providers
from flask import Flask

from fiar import cli, routes
from fiar.di.providers.repositories import UserRepoProvider, RequestRepoProvider, FriendshipRepoProvider, \
    GameRepoProvider, InviteRepoProvider
from fiar.di.providers.services import HashServiceProvider, UidServiceProvider, UserServiceProvider, \
    AuthServiceProvider, TokenServiceProvider, PswdTokenServiceProvider, MailServiceProvider, FriendshipServiceProvider, \
    GameServiceProvider
from fiar.di.providers.sqlalchemy import SqlAlchemyDbProvider


class AppContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()

    app = providers.Dependency(instance_of=Flask)

    # --- DB ---
    sqlalchemy_db = providers.Resource(SqlAlchemyDbProvider, app)

    # --- Repos ---
    user_repo = providers.Resource(UserRepoProvider, app, sqlalchemy_db)
    friendship_repo = providers.Resource(FriendshipRepoProvider, app, sqlalchemy_db)
    request_repo = providers.Resource(RequestRepoProvider, app, sqlalchemy_db)
    game_repo = providers.Resource(GameRepoProvider, app, sqlalchemy_db)
    invite_repo = providers.Resource(InviteRepoProvider, app, sqlalchemy_db)

    # --- Util services ---
    mail_service = providers.Resource(MailServiceProvider, app)
    hash_service = providers.Resource(HashServiceProvider, app)
    uid_service = providers.Resource(UidServiceProvider, app, user_repo)
    auth_service = providers.Resource(AuthServiceProvider, app, user_repo, hash_service)
    token_service = providers.Resource(TokenServiceProvider, app)
    pswd_token_service = providers.Resource(PswdTokenServiceProvider, app, token_service, user_repo)

    # --- Entity services ---
    user_service = providers.Resource(UserServiceProvider, app, user_repo, uid_service, hash_service)
    friendship_service = providers.Resource(FriendshipServiceProvider, app, friendship_repo, request_repo)
    game_service = providers.Resource(GameServiceProvider, app, game_repo, invite_repo)


def init_container(app: Flask):
    app.container = AppContainer(app=app)

    # wire all di dependencies
    app.container.wire(packages=[
        routes
    ], modules=[
        cli
    ])
