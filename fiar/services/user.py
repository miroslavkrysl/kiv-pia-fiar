from datetime import datetime

from fiar.db import User
from fiar.repositories.user import UserRepo
from fiar.services.hash import HashService
from fiar.services.uid import UidService


class UserService:
    """
    Various user logic.
    """

    def __init__(self,
                 user_repo: UserRepo,
                 uid_service: UidService,
                 hash_service: HashService):
        self.user_repo = user_repo
        self.uid_service = uid_service
        self.hash_service = hash_service

    def change_password(self, user: User, password: str):
        """
        Change the users password.
        :param user: The user.
        :param password: New password.
        """
        hash = self.hash_service.hash(password)
        user.password = hash

    def update_last_active_at(self, user: User, last_active_at=None):
        """
        Update the users last_active_at time.
        :param user: The user.
        :param last_active_at: If none, datetime.now() is used.
        """
        last_active_at = last_active_at if last_active_at is not None else datetime.now()
        user.last_active_at = last_active_at

    def create_user(self, **kwargs) -> User:
        """
        Create a new user from given dict and save him.
        :param kwargs: The user named fields values.
        :return: The created user.
        """
        user = dict(kwargs)

        user['password'] = self.hash_service.hash(user['password'])
        user['uid'] = self.uid_service.make_uid()

        if 'is_admin' not in user:
            user['is_admin'] = False

        if 'last_active_at' not in user:
            user['last_active_at'] = datetime.min

        return self.user_repo.add(**user)

    def change_uid(self, user: User):
        """
        Change the user uid.
        :param user: The user.
        """
        uid = self.uid_service.make_uid()
        user.uid = uid
