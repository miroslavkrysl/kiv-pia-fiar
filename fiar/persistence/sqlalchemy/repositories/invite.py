from fiar.data.models import Invite
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb


class InviteRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def add(self, invite: Invite):
        session = self.db.session
        session.add(invite)

    def delete(self, invite: Invite):
        session = self.db.session
        session.delete(invite)