from typing import List

from fiar.persistence.db import Database
from fiar.persistence.models import User


class UserRepository:

    def __init__(self, db: Database):
        self.db = db

    def all(self) -> List[User]:
        return self.db.session.query(User).all()

    def add(self, user: User):
        self.db.session.add(user)
        self.db.session.commit()

    # def all_online(self) -> List[User]:
    #     return self.User.select()
