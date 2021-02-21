from typing import Iterable, Optional

from fiar.data.models import Friendship, User
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb


class FriendshipRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_by_users(self, user: User, friend: User) -> Optional[Friendship]:
        session = self.db.session
        return session.query(Friendship).filter_by(sender=user, recipient=friend).first()

    def get_all_by_user(self, user: User) -> Iterable[Friendship]:
        """
        Get all friendships of given user.
        :param user: User.
        :return: All friendships of user.
        """
        session = self.db.session
        return session.query(Friendship).filter_by(sender=user)

    def add(self, friendship: Friendship):
        """
        Add friendship. Also add bidirectional friendship.
        :param friendship: Friendship.
        """
        session = self.db.session
        inverse = Friendship(friendship.recipient_id, friendship.sender_id)
        session.add(friendship)
        session.add(inverse)

    def delete(self, friendship: Friendship):
        """
        Add friendship. Also delete bidirectional friendship.
        :param friendship: Friendship.
        """
        session = self.db.session

        inverse = session.query(Friendship).filter_by(sender_id=friendship.recipient_id,
                                                      recipient_id=friendship.sender_id).first()
        if inverse:
            session.delete(inverse)

        session.delete(friendship)
