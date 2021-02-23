from typing import Iterable

from sqlalchemy import and_

from fiar.data.models import Game, Move
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.persistence.sqlalchemy.orm import move_table


class MoveRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_all_by_game(self, game: Game) -> Iterable[Move]:
        session = self.db.session
        return session.query(Move).filter_by(game=game)

    def count_by_game(self, game: Game) -> int:
        session = self.db.session
        return session.query(Move).filter_by(game=game).count()

    def get_by_game_and_pos(self, game: Game, row: int, col: int) -> Move:
        session = self.db.session
        return session.query(Move).filter(and_(
            move_table.c.game_id == game.id,
            move_table.c.row == row,
            move_table.c.col == col)).first()

    def add(self, move: Move):
        session = self.db.session
        session.add(move)
        session.commit()

    def delete(self, move: Move):
        session = self.db.session
        session.delete(move)
        session.commit()
