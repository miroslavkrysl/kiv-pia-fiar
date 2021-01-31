import enum
from datetime import datetime

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True)
    email = Column(String(254), unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    last_active_at = Column(DateTime, default=datetime.now, nullable=False)
    active_game_id = Column(Integer, ForeignKey('game.id', use_alter=True, name='fk_user_active_game_id'), default=None, nullable=True)

    # for login/logout purposes
    # not stable value, can be changed over time
    uid = Column(String(64), nullable=False, unique=True)

    active_game = relationship("Game", foreign_keys="User.active_game_id")


class Friendship(Base):
    __tablename__ = 'friendship'
    from_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    to_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    from_user = relationship("User", foreign_keys="Friendship.from_user_id")
    to_user = relationship("User", foreign_keys="Friendship.to_user_id")


class FriendshipRequest(Base):
    __tablename__ = 'friendship_request'
    from_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    to_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    from_user = relationship("User", foreign_keys="FriendshipRequest.from_user_id")
    to_user = relationship("User", foreign_keys="FriendshipRequest.to_user_id")


class Invitation(Base):
    __tablename__ = 'invitation'
    from_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    to_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    from_user = relationship("User", foreign_keys="Invitation.from_user_id")
    to_user = relationship("User", foreign_keys="Invitation.to_user_id")


class Player(enum.Enum):
    O = 0
    X = 1


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_o_id = Column(Integer, ForeignKey('user.id', use_alter=True, name='fk_game_player_o_id'), nullable=False)
    player_x_id = Column(Integer, ForeignKey('user.id', use_alter=True, name='fk_game_player_x_id'), nullable=False)

    player_o = relationship("User", foreign_keys=[player_o_id])
    player_x = relationship("User", foreign_keys=[player_x_id])
    result = relationship('GameResult', uselist=False)

    __table_args__ = (
        UniqueConstraint('id', 'player_o_id', 'player_x_id'),
    )


class Move(Base):
    __tablename__ = 'move'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player = Column(Enum(Player), nullable=False)
    pos_x = Column(Integer, nullable=False)
    pos_y = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('player', 'pos_x', 'pos_y'),
    )


class GamesMoves(Base):
    __tablename__ = 'games_moves'
    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    move_id = Column(Integer, ForeignKey('move.id'), primary_key=True)

    game = relationship('Game')
    move = relationship('Move')

    __table_args__ = (
        UniqueConstraint('game_id', 'move_id'),
    )


class GameResult(Base):
    __tablename__ = 'game_result'
    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    winner_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    game = relationship('Game', uselist=False)
    winner = relationship('User', uselist=False)
