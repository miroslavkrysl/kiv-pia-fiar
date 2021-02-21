from typing import Optional, Iterable

from fiar.data.models import Invite, User
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.persistence.sqlalchemy.orm import invite_table, user_table


class InviteRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_by_users(self, sender: User, recipient: User) -> Optional[Invite]:
        session = self.db.session
        return session.query(Invite).filter_by(sender=sender, recipient=recipient).first()

    def get_all_sent_by_user(self, user: User) -> Iterable[Invite]:
        session = self.db.session
        return session.query(Invite).filter_by(sender=user)

    def get_all_received_by_user(self, user: User) -> Iterable[Invite]:
        session = self.db.session
        return session.query(Invite).filter_by(recipient=user)

    def get_all_users_send_by(self, user: User) -> Iterable[User]:
        """
        Get all users that has been invited by the given user.
        :param user: User.
        :return: All users that has been invited by the given user.
        """
        session = self.db.session
        return session.query(User) \
            .join(Invite, invite_table.c.recipient_id == user_table.c.id) \
            .filter(invite_table.c.sender_id == user.id)

    def get_all_users_received_by(self, user: User) -> Iterable[User]:
        """
        Get all users that has invited the given user.
        :param user: User.
        :return: All users that has invited the given user.
        """
        session = self.db.session
        return session.query(User) \
            .join(Invite, invite_table.c.sender_id == user_table.c.id) \
            .filter(invite_table.c.recipient_id == user.id)

    def add(self, invite: Invite):
        session = self.db.session
        session.add(invite)

    def delete(self, invite: Invite):
        session = self.db.session
        session.delete(invite)