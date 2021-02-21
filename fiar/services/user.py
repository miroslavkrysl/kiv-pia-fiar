from datetime import datetime, timedelta

from fiar.data.models import User
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.services.hash import HashService
from fiar.services.uid import UidService


class UserService:
    """
    Various user logic.
    """

    def __init__(self,
                 user_repo: UserRepo,
                 uid_service: UidService,
                 hash_service: HashService,
                 online_timeout: timedelta):
        self.user_repo = user_repo
        self.uid_service = uid_service
        self.hash_service = hash_service
        self.online_timeout = online_timeout

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

    def create_user(self,
                    username: str,
                    email: str,
                    password: str,
                    is_admin: bool = False,
                    last_active_at: datetime = None) -> User:
        """
        Create user from the given keyword parameters, initialize non-required and secret fields.
        :return: New user.
        """
        password = self.hash_service.hash(password)
        uid = self.uid_service.make_uid()

        user = User(uid, username, email, password, is_admin, last_active_at)
        self.user_repo.add(user)

        return user

    def change_uid(self, user: User):
        """
        Change the user uid.
        :param user: The user.
        """
        uid = self.uid_service.make_uid()
        user.uid = uid

    def username_exists(self, username: str) -> bool:
        return self.user_repo.get_by_username(username) is not None

    def email_exists(self, email: str) -> bool:
        return self.user_repo.get_by_email(email) is not None
