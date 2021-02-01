import click
from dependency_injector.wiring import inject, Provide
from flask import Flask
from flask.cli import with_appcontext
import passlib.totp

from fiar.di import Container
from fiar.utils import load_config, store_config


def register_commands(app: Flask):
    # app.cli.add_command(init_db_command)
    app.cli.add_command(key_generate)


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


# @click.command('db:init')
# @with_appcontext
# def init_db_command():
#     from fiar import container
#     db = container.database()
#     db.create_tables(Base)
#     click.echo('Database initialized.')
#
#
# @click.command('db:fill')
# @with_appcontext
# def fill_db_command():
#     fill_db()
#     click.echo('Database filled.')
