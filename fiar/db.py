from datetime import datetime

from flask import Flask, g
from pony.orm import *

database = Database()


class User(database.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, 32, unique=True)
    email = Required(str, 255, unique=True)
    password = Required(str, 100)
    is_admin = Required(bool)
    uid = Required(str, 128, unique=True)
    last_active_at = Required(datetime)


# import enum
# from datetime import datetime
#
# from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum, UniqueConstraint, DateTime, inspect
# from sqlalchemy.ext.declarative import declarative_base, as_declarative
#
#
# @as_declarative()
# class Base:
#     def to_dict(self):
#         return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
#
#
# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(32), unique=True)
#     email = Column(String(254), unique=True)
#     password = Column(String(255), nullable=False)
#     is_admin = Column(Boolean, default=False, nullable=False)
#     last_active_at = Column(DateTime, default=datetime.now, nullable=False)
#     active_game_id = Column(Integer, ForeignKey('game.id', use_alter=True, name='fk_user_active_game_id'), default=None, nullable=True)
#     uid = Column(String(64), nullable=False, unique=True)

# active_game = relationship("Game", foreign_keys="User.active_game_id")


# class Friendship(Base):
#     __tablename__ = 'friendship'
#     from_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#     to_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#
#     # from_user = relationship("User", foreign_keys="Friendship.from_user_id")
#     # to_user = relationship("User", foreign_keys="Friendship.to_user_id")
#
#
# class FriendshipRequest(Base):
#     __tablename__ = 'friendship_request'
#     from_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#     to_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#
#     # from_user = relationship("User", foreign_keys="FriendshipRequest.from_user_id")
#     # to_user = relationship("User", foreign_keys="FriendshipRequest.to_user_id")
#
#
# class Invitation(Base):
#     __tablename__ = 'invitation'
#     from_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#     to_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#
#     # from_user = relationship("User", foreign_keys="Invitation.from_user_id")
#     # to_user = relationship("User", foreign_keys="Invitation.to_user_id")
#
#
# class Player(enum.Enum):
#     O = 0
#     X = 1
#
#
# class Game(Base):
#     __tablename__ = 'game'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     player_o_id = Column(Integer, ForeignKey('user.id', use_alter=True, name='fk_game_player_o_id'), nullable=False)
#     player_x_id = Column(Integer, ForeignKey('user.id', use_alter=True, name='fk_game_player_x_id'), nullable=False)
#
#     # player_o = relationship("User", foreign_keys=[player_o_id])
#     # player_x = relationship("User", foreign_keys=[player_x_id])
#     # result = relationship('GameResult', uselist=False)
#
#     __table_args__ = (
#         UniqueConstraint('id', 'player_o_id', 'player_x_id'),
#     )
#
#
# class Move(Base):
#     __tablename__ = 'move'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     player = Column(Enum(Player), nullable=False)
#     pos_x = Column(Integer, nullable=False)
#     pos_y = Column(Integer, nullable=False)
#
#     __table_args__ = (
#         UniqueConstraint('player', 'pos_x', 'pos_y'),
#     )
#
#
# class GamesMoves(Base):
#     __tablename__ = 'games_moves'
#     game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
#     move_id = Column(Integer, ForeignKey('move.id'), primary_key=True)
#
#     game = relationship('Game')
#     move = relationship('Move')
#
#     __table_args__ = (
#         UniqueConstraint('game_id', 'move_id'),
#     )
#
#
# class GameResult(Base):
#     __tablename__ = 'game_result'
#     game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
#     winner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#
#     game = relationship('Game', uselist=False)
#     winner = relationship('User', uselist=False)


class Db:
    G_PREFIX = 'db_'
    G_SESSION = G_PREFIX + 'session'

    def __init__(self, app: Flask):
        db_config = app.config['DATABASE']
        database.bind(provider=db_config['PROVIDER'],
                      user=db_config['USER'],
                      password=db_config['PASSWORD'],
                      host=db_config['HOST'],
                      database=db_config['NAME'])
        database.generate_mapping(check_tables=False)

        self.database = database

        app.before_request(self.enter_session)
        app.teardown_appcontext(lambda e: self.exit_session(e))

    def enter_session(self):
        if not hasattr(g, self.G_SESSION):
            session = db_session()
            session.__enter__()
            setattr(g, self.G_SESSION, session)

    def exit_session(self, exc=None):
        if hasattr(g, self.G_SESSION):
            session = getattr(g, self.G_SESSION)
            session.__exit__(exc=exc)
            delattr(g, self.G_SESSION)
