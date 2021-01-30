from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Database:
    def __init__(self, app: Flask):
        self.engine = create_engine(app.config['APP_DB_URI'])
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))
        self.session = None

        @app.before_request
        def create_session():
            self.session = self.session_factory()
            return None

        @app.after_request
        def remove_session(response):
            self.session_factory.remove()
            self.session = None
            return response


def init_db(database: Database):
    """
    Clear the existing table and data in database
    and create new tables.
    """
    from fiar.persistence.models import Base

    # Base.metadata.drop_all(bind=database.engine)
    Base.metadata.create_all(bind=database.engine)
