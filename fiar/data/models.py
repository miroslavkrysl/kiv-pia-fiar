from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional


@dataclass
class User:
    id: int = field(init=False)
    uid: str
    username: str
    email: str
    password: str
    is_admin: bool = field(default=False)
    last_active_at: Optional[datetime] = field(default=None)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, self.__class__) and self.id == o.id


@dataclass
class Game:
    id: int = field(init=False)
    player_o_id: int
    player_x_id: int
    on_turn: int = field(default=0)
    winner: Optional[int] = field(default=None)


@dataclass
class Move:
    game_id: int
    side: int
    row: int
    col: int


@dataclass
class Invite:
    sender_id: int
    recipient_id: int


@dataclass
class Request:
    sender_id: int
    recipient_id: int


@dataclass
class Friendship:
    sender_id: int
    recipient_id: int


class MoveResult(Enum):
    OK = 'ok'
    OUT = 'out'
    OCCUPIED = 'occupied'
    DRAW = 'draw'
    WINNER = 'win'


SIDE_O = 0
SIDE_X = 1
SIDE_DRAW = 2
