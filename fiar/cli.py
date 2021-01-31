import click
from flask import Flask
from flask.cli import with_appcontext

from fiar.persistence.models import Base


def register_commands(app: Flask):
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    from fiar import container
    db = container.database
    db.create_tables(Base)
    click.echo('Database initialized.')