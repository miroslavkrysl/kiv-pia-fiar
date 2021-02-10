from typing import Iterable

from pony.orm import flush

from fiar.db import User, Friendship, Game, GameInvite


class GameRepo:
    def __init__(self):
        pass

    def _get_all_of(self, user: User):
        return Game.select(lambda g: g.player_o == user or g.player_x == user)

    def get_by_id(self, id: int) -> Game:
        return GameInvite.get(id=id)

    def get_all_finished_of(self, user: User) -> Iterable[Game]:
        return self._get_all_of(user).where(lambda g: g.winner is not None)

    def get_all_unfinished_of(self, user: User) -> Iterable[Game]:
        return self._get_all_of(user).where(lambda g: g.winner is None)

    def create(self, user: User, friend: User):
        Friendship(sender=user, recipient=friend)
        flush()
