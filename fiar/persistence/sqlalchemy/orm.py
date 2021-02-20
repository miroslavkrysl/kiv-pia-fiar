from sqlalchemy import MetaData, Table, Column, DateTime, Integer, String, Boolean, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm.decl_api import registry

from fiar.data.models import User, Player, Game, Move, Friendship, FriendshipRequest, Invite

metadata = MetaData()
mapper_registry = registry()

# --- User ---

user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('uid', String(128), unique=True, nullable=False),
    Column('username', String(16), unique=True, nullable=False),
    Column('email', String(256), unique=True, nullable=False),
    Column('password', String(128), nullable=False),
    Column('is_admin', Boolean, nullable=False),
    Column('last_active_at', DateTime)
)

mapper_registry.map_imperatively(User, user_table)

# --- Game ---

game_table = Table(
    'game', metadata,
    Column('id', Integer, primary_key=True),
    Column('player_o_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('player_x_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('started_at', DateTime, nullable=False),
    Column('ended_at', DateTime),
    Column('winner', Enum(Player))
)

mapper_registry.map_imperatively(Game, game_table, properties={
    'player_o': relationship(User, backref='games_as_o'),
    'player_x': relationship(User, backref='games_as_x')
})

# --- Move ---

move_table = Table(
    'move', metadata,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer, ForeignKey('game.id'), nullable=False),
    Column('player', Enum(Player), nullable=False),
    Column('row', Integer, nullable=False),
    Column('col', Integer, nullable=False),
    UniqueConstraint('game_id', 'player', 'row', 'col')
)

mapper_registry.map_imperatively(Move, move_table, properties={
    'game': relationship(Game, backref='moves'),
})

# --- Invite ---

invite_table = Table(
    'invite', metadata,
    Column('sender_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('recipient_id', Integer, ForeignKey('user.id'), primary_key=True),
)

mapper_registry.map_imperatively(Invite, invite_table, properties={
    'sender': relationship(User, backref='invites_sent'),
    'recipient': relationship(User, backref='invites_received')
})

# --- FriendshipRequest ---

friendship_request_table = Table(
    'friendship_request', metadata,
    Column('sender_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('recipient_id', Integer, ForeignKey('user.id'), primary_key=True),
)

mapper_registry.map_imperatively(FriendshipRequest, friendship_request_table, properties={
    'sender': relationship(User, backref='friendship_requests_sent'),
    'recipient': relationship(User, backref='friendship_requests_received')
})

# --- Friendship ---

friendship_table = Table(
    'friendship', metadata,
    Column('sender_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('recipient_id', Integer, ForeignKey('user.id'), primary_key=True),
)

mapper_registry.map_imperatively(Friendship, friendship_table, properties={
    'sender': relationship(User, backref='friendship_sent'),
    'recipient': relationship(User, backref='friendship_received')
})
