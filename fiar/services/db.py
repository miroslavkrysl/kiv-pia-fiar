from flask import Flask, g
from pony.orm import db_session

from fiar.db import Database


class Db:
    G_PREFIX = 'db_'
    G_SESSION = G_PREFIX + 'session'

    def __init__(self, app: Flask, database: Database):
        db_config = app.config['DATABASE']
        database.bind(provider=db_config['PROVIDER'],
                      user=db_config['USER'],
                      password=db_config['PASSWORD'],
                      host=db_config['HOST'],
                      database=db_config['NAME'])
        database.generate_mapping(check_tables=False)

        self.database = database

        app.before_request(self.enter_session)
        app.teardown_appcontext(lambda e: self.exit_session(e))

    def enter_session(self):
        if not hasattr(g, self.G_SESSION):
            session = db_session()
            session.__enter__()
            setattr(g, self.G_SESSION, session)

    def exit_session(self, exc=None):
        if hasattr(g, self.G_SESSION):
            session = getattr(g, self.G_SESSION)
            session.__exit__(exc=exc)
            delattr(g, self.G_SESSION)
