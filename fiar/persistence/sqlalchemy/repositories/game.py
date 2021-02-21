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

    def get_all_by_player_o(self, user: User, ended: Optional[bool] = None) -> Iterable[Game]:
        session = self.db.session
        query = session.query(Game).filter_by(player_o=user)

        if ended is not None:
            if ended:
                query = query.filter(game_table.c.ended_at != None)
            else:
                query = query.filter(game_table.c.ended_at == None)

        return query

    def get_all_by_player_x(self, user: User, ended: Optional[bool] = None) -> Iterable[User]:
        session = self.db.session
        query = session.query(Game).filter_by(player_x=user)

        if ended is not None:
            if ended:
                query = query.filter(game_table.c.ended_at != None)
            else:
                query = query.filter(game_table.c.ended_at == None)

        return query

    def get_all_by_player(self, user: User, ended: Optional[bool] = None) -> Iterable[User]:
        session = self.db.session
        query = session.query(Game).filter(or_(
            game_table.c.player_o_id == user.id,
            game_table.c.player_x_id == user.id,
        ))

        if ended is not None:
            if ended:
                query = query.filter(game_table.c.ended_at != None)
            else:
                query = query.filter(game_table.c.ended_at == None)

        return query

    def add(self, game: Game):
        session = self.db.session
        session.add(game)

    def delete(self, game: Game):
        session = self.db.session
        session.delete(game)
