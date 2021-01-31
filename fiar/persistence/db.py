from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from fiar.persistence.models import Base


class Database:
    def __init__(self, uri: str):
        self.engine = create_engine(uri)
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))
        self.session = None

    def start_session(self) -> Session:
        if self.session is None:
            self.session = self.session_factory()

        return self.session

    def end_session(self):
        if self.session is not None:
            self.session_factory.remove()
            self.session = None

    def create_tables(self, base: Base):
        """
        Clear the existing table and data in database
        and create new tables.
        """

        # Base.metadata.drop_all(bind=self.engine)
        base.metadata.create_all(bind=self.engine)


def initialize_db(app: Flask):
    uri = app.config['DB_URI']
    database = Database(uri)

    @app.before_request
    def start_session():
        database.start_session()

    @app.teardown_appcontext
    def end_session(exception):
        database.end_session()

    return database
