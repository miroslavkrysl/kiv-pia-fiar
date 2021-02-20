from typing import Iterable, Optional

from fiar.data.models import FriendshipRequest, User
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.persistence.sqlalchemy.orm import friendship_request_table, user_table


class FriendshipRequestRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_by_users(self, sender: User, recipient: User) -> Optional[FriendshipRequest]:
        session = self.db.session
        return session.query(FriendshipRequest).filter_by(sender=sender, recipient=recipient).first()

    def get_all_sent_by_user(self, user: User) -> Iterable[FriendshipRequest]:
        session = self.db.session
        return session.query(FriendshipRequest).filter_by(sender=user)

    def get_all_received_by_user(self, user: User) -> Iterable[FriendshipRequest]:
        session = self.db.session
        return session.query(FriendshipRequest).filter_by(recipient=user)

    def get_all_users_requested_by(self, user: User) -> Iterable[User]:
        """
        Get all users that given user has requested a friendship.
        :param user: User.
        :return: All users that given user has requested a friendship.
        """
        session = self.db.session
        return session.query(User) \
            .join(FriendshipRequest, friendship_request_table.c.recipient_id == user_table.c.id) \
            .filter(friendship_request_table.c.sender_id == user.id)

    def get_all_users_received_by(self, user: User) -> Iterable[User]:
        """
        Get all users that has requested given user a friendship.
        :param user: User.
        :return: All users that has requested given user a friendship.
        """
        session = self.db.session
        return session.query(User) \
            .join(FriendshipRequest, friendship_request_table.c.sender_id == user_table.c.id) \
            .filter(friendship_request_table.c.recipient_id == user.id)

    def add(self, friendship_request: FriendshipRequest):
        session = self.db.session
        session.add(friendship_request)

    def delete(self, friendship_request: FriendshipRequest):
        session = self.db.session
        session.delete(friendship_request)
