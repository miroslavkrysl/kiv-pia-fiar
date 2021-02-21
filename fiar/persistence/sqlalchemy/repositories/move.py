from typing import Iterable

from fiar.data.models import Game, Move
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb


class MoveRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_all_by_game(self, game: Game) -> Iterable[Move]:
        session = self.db.session
        return session.query(Move).filter_by(game=game)

    def get_by_game_and_pos(self, game: Game, row: int, col: int) -> Move:
        session = self.db.session
        return session.query(Move).filter_by(game=game, row=row, col=col)

    def add(self, game: Move):
        session = self.db.session
        session.add(game)

    def delete(self, game: Move):
        session = self.db.session
        session.delete(game)
