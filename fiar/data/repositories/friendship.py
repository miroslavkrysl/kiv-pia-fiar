from typing import Iterable, Optional

from fiar.data.models import Friendship, User
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.persistence.sqlalchemy.orm import friendship_table, user_table


class FriendshipRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_by_users(self, sender: User, recipient: User) -> Optional[Friendship]:
        session = self.db.session
        return session.query(Friendship).filter_by(sender=sender, recipient=recipient).first()

    def get_all_sent_by_user(self, user: User) -> Iterable[Friendship]:
        session = self.db.session
        return session.query(Friendship).filter_by(sender=user)

    def get_all_friends_sent_by(self, user: User) -> Iterable[User]:
        """
        Get all friends of given user.
        :param user: User.
        :return: All friends of user.
        """
        session = self.db.session
        return session.query(User) \
            .join(Friendship, friendship_table.c.recipient_id == user_table.c.id) \
            .filter(friendship_table.c.sender_id == user.id)

    def add(self, friendship: Friendship):
        session = self.db.session
        session.add(friendship)

    def delete(self, friendship: Friendship):
        session = self.db.session
        session.delete(friendship)
