import click
from dependency_injector.wiring import inject, Provide
from flask import Flask
from flask.cli import with_appcontext
import passlib.totp

from fiar.di import Container
from fiar.repositories.user import UserRepo
from fiar.services.db import Db
from fiar.services.user import UserService
from fiar.utils import load_config, store_config, with_request_context


def register_commands(app: Flask):
    app.cli.add_command(key_generate)
    app.cli.add_command(db_init_command)
    app.cli.add_command(db_drop_command)
    app.cli.add_command(db_fill_command)


@click.command('key:generate')
@with_appcontext
@inject
def key_generate(app: Flask = Provide[Container.app]):
    key = passlib.totp.generate_secret()
    config = load_config(app)

    old_key = config.get('SECRET_KEY')
    config['SECRET_KEY'] = key

    if old_key is not None:
        if config.get('OLD_SECRET_KEYS') is None:
            config['OLD_SECRET_KEYS'] = []

        config['OLD_SECRET_KEYS'].append(old_key)

    store_config(app, config)
    click.echo('New key generated.')


@click.command('db:drop')
@with_appcontext
@inject
def db_drop_command(db: Db = Provide[Container.db]):
    db.database.drop_all_tables(with_all_data=True)
    click.echo('All app related database tables dropped.')


@click.command('db:init')
@with_appcontext
@inject
def db_init_command(db: Db = Provide[Container.db]):
    db.database.create_tables()
    click.echo('All database tables created.')


@click.command('db:fill')
@with_appcontext
@with_request_context
@inject
def db_fill_command(user_service: UserService = Provide[Container.user_service],
                    user_repo: UserRepo = Provide[Container.user_repo]):
    user_repo.create(**user_service.init_user(username='hello',
                                              email='hello@example.com',
                                              password='password'))

    user_repo.create(**user_service.init_user(username="jello",
                                              email="jello@example.com",
                                              password="password"))

    user_repo.create(**user_service.init_user(username="mkrysl",
                                              email="mkrysl@protonmail.com",
                                              password="password"))

    click.echo('Database filled with example data.')
