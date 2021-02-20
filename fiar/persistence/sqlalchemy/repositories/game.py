from fiar.data.models import Game
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb


class GameRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def add(self, game: Game):
        session = self.db.session
        session.add(game)

    def delete(self, game: Game):
        session = self.db.session
        session.delete(game)
