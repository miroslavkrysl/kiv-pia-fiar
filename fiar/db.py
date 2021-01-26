import click
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from fiar.config import APP_DB_URI


class Db:
    def __init__(self, db_uri: str) :
        self.engine = create_engine(db_uri)
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    from fiar.models import Base

    db = Db(APP_DB_URI)
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)

    click.echo('Database initialized.')
