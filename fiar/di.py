from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from flask import Flask, request, Config, g
from flask_socketio import SocketIO
from pony.orm import Database, db_session

from fiar.db import database


class Container(containers.DeclarativeContainer):
    container_config = providers.Configuration()

    app = providers.Dependency(instance_of=Flask)

    # --- Database ---
    db = providers.Object(database)

    # --- websockets - Socket.IO ---
    socket_io = providers.Singleton(
        SocketIO,
        app
    )

    # --- Request ---
    request = providers.Resource(lambda: request)

    # --- Repositories ---
    # user_dao = providers.Singleton(
    #     UserDao,
    #     database,
    # )
    #
    # # --- Services ---
    #
    # hash_service = providers.Singleton(
    #     HashService
    # )
    #
    # uid_service = providers.Singleton(
    #     UidService,
    #     user_dao,
    #     config.UID_LENGTH
    # )
    #
    # auth_service = providers.Singleton(
    #     AuthService,
    #     app,
    #     user_dao
    # )


def create_container(app: Flask):
    container = Container(app=app)
    app = container.app()

    app.before_first_request(before_first_request)
    app.before_request(before_request)
    app.teardown_appcontext(teardown_appcontext)

    return container


@inject
def before_first_request(container: Container = Provide[Container],
                         app: Flask = Provide[Container.app],
                         db: Database = Provide[Container.db]):
    # setup database connection
    db_config = app.config['DATABASE']
    db.bind(provider=db_config['PROVIDER'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            database=db_config['NAME'])
    db.generate_mapping(create_tables=True)

    # setup session variable
    container.db_session = None


@inject
def before_request(container: Container = Provide[Container]):
    # setup the request instance
    container.request.init()

    # setup the database session
    container.db_session = db_session().__enter__()


@inject
def teardown_appcontext(exception,
                        container: Container = Provide[Container]):
    # end the database session
    if getattr(container, 'db_session', None) is not None:
        container.db_session.__exit__()
        container.db_session = None
