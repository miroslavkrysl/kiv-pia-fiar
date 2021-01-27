import click
from flask import Flask
from flask.cli import with_appcontext
from injector import inject

from fiar.persistence.db import Database, init_db


def register_commands(app: Flask):
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    from fiar import di
    db = di.injector.get(Database)
    init_db(db)
    click.echo('Database initialized.')
