from typing import Optional, Iterable

from sqlalchemy import or_

from fiar.data.models import Game, User
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.persistence.sqlalchemy.orm import game_table


class GameRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_by_id(self, id: int) -> Game:
        session = self.db.session
        return session.query(Game).filter_by(id=id).first()

    def get_by_players(self, player_o: User, player_x: User) -> Optional[Game]:
        session = self.db.session
        return session.query(Game).filter_by(player_o=player_o, player_x=player_x).first()

    def get_all_by_player(self, user: User) -> Iterable[Game]:
        session = self.db.session
        return session.query(Game).filter(or_(
            game_table.c.player_o_id == user.id,
            game_table.c.player_x_id == user.id,
        ))

    def add(self, game: Game):
        session = self.db.session
        session.add(game)
        session.commit()

    def delete(self, game: Game):
        session = self.db.session
        session.delete(game)
        session.commit()

    def update(self):
        self.db.session.commit()
