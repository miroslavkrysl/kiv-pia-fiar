from datetime import datetime
from enum import IntEnum

from pony.orm import *

database = Database()


class Player(IntEnum):
    O = 0
    X = 1


class User(database.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, 32, unique=True)
    email = Required(str, 255, unique=True)
    password = Required(str, 60)
    is_admin = Required(bool)
    uid = Required(str, 128, unique=True)
    last_active_at = Required(datetime)
    last_playing_at = Required(datetime)

    sent_friendship_requests = Set('FriendshipRequest', reverse='sender')
    received_friendship_requests = Set('FriendshipRequest', reverse='recipient')
    sent_game_invites = Set('GameInvite', reverse='sender')
    received_game_invites = Set('GameInvite', reverse='recipient')
    sent_friendships = Set('Friendship', reverse='sender')
    received_friendships = Set('Friendship', reverse='recipient')
    games_as_o = Set('Game', reverse='player_o')
    games_as_x = Set('Game', reverse='player_x')


class Game(database.Entity):
    id = PrimaryKey(int, auto=True)
    moves = Set('Move')
    player_o = Required(User, reverse='games_as_o')
    player_x = Required(User, reverse='games_as_x')
    winner = Optional(int)


class Move(database.Entity):
    id = PrimaryKey(int, auto=True)
    player = Required(int)
    x = Required(int)
    y = Required(int)
    games = Set(Game)

    composite_key(player, x, y)


class FriendshipRequest(database.Entity):
    id = PrimaryKey(int, auto=True)
    sender = Required(User, reverse='sent_friendship_requests')
    recipient = Required(User, reverse='received_friendship_requests')

    composite_key(sender, recipient)


class GameInvite(database.Entity):
    id = PrimaryKey(int, auto=True)
    sender = Required(User, reverse='sent_game_invites')
    recipient = Required(User, reverse='received_game_invites')

    composite_key(sender, recipient)


class Friendship(database.Entity):
    id = PrimaryKey(int, auto=True)
    sender = Required(User, reverse='sent_friendships')
    recipient = Required(User, reverse='received_friendships')

    composite_key(sender, recipient)
