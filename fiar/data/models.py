from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
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
    player_o_last_active_at: Optional[datetime]
    player_x_last_active_at: Optional[datetime]
    winner: Optional[int] = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = field(default=None)


@dataclass
class Move:
    id: int = field(init=False)
    game_id: int
    player: int
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
