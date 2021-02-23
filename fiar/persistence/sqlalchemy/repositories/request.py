from typing import Iterable, Optional

from sqlalchemy import or_

from fiar.data.models import Request, User
from fiar.persistence.sqlalchemy.db import SqlAlchemyDb
from fiar.persistence.sqlalchemy.orm import request_table


class RequestRepo:
    def __init__(self, db: SqlAlchemyDb):
        self.db = db

    def get_by_users(self, sender: User, recipient: User) -> Optional[Request]:
        session = self.db.session
        return session.query(Request).filter_by(sender=sender, recipient=recipient).first()

    def get_all_by_user(self, user: User) -> Iterable[Request]:
        session = self.db.session
        return session.query(Request).filter(or_(
            request_table.c.sender_id == user.id,
            request_table.c.recipient_id == user.id))

    def add(self, request: Request):
        session = self.db.session
        session.add(request)
        session.commit()

    def delete(self, request: Request):
        session = self.db.session
        session.delete(request)
        session.commit()
