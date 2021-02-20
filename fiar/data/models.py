from dataclasses import dataclass, field
from datetime import datetime
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


class Player(Enum):
    O = 'o'
    X = 'x'


@dataclass
class Game:
    id: int = field(init=False)
    player_o_id: int
    player_x_id: int
    player_o_last_active_at: Optional[datetime]
    player_x_last_active_at: Optional[datetime]
    winner: Optional[Player] = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = field(default=None)


@dataclass
class Move:
    id: int = field(init=False)
    game_id: int
    player: Player
    row: int
    col: int


@dataclass
class Invite:
    sender_id: int
    recipient_id: int


@dataclass
class FriendshipRequest:
    sender_id: int
    recipient_id: int


@dataclass
class Friendship:
    sender_id: int
    recipient_id: int
