from typing import Optional

from flask import session, g

from fiar.data.models import User
from fiar.data.repositories.user import UserRepo
from fiar.services.hash import HashService


class AuthService:
    """
    Takes care of authenticating users, login and logout within the session
    as well as loading the currently logged user from the session.
    """

    SESSION_UID = 'user_uid'
    G_PREFIX = 'auth_'
    G_USER = G_PREFIX + 'user'

    def __init__(self, user_repo: UserRepo, hash_service: HashService):
        self.user_repo = user_repo
        self.hash_service = hash_service

    def auth_email_password(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate the user by email and password.
        :param email: Email.
        :param password: Raw password.
        :return: The authenticated user or None on fail.
        """
        user = self.user_repo.get_by_email(email)

        if user is None:
            return None

        if not self.hash_service.verify(password, user.password):
            return None

        return user

    def login(self, user: User):
        """
        Login the user within the session.
        :param user: The user instance.
        """
        session[self.SESSION_UID] = user.uid
        self._set_user(user)

    def logout(self):
        """
        Logout the user from the session.
        """
        if self.SESSION_UID in session:
            session.pop(self.SESSION_UID)

        self._set_user(None)

    def get_user(self) -> Optional[User]:
        """
        Get the currently logged user from the session.
        """
        return self._get_user()

    def is_authenticated(self) -> bool:
        """
        Check if the current user is authenticated.
        """
        return self._get_user() is not None

    def _set_user(self, user: Optional[User]):
        setattr(g, self.G_USER, user)

    def _get_user(self) -> User:
        if not hasattr(g, self.G_USER):
            user = self._load_user()
            self._set_user(user)
            return user

        return getattr(g, self.G_USER)

    def _load_user(self):
        user_uid = session.get(self.SESSION_UID)

        if user_uid is not None:
            user = self.user_repo.get_by_uid(user_uid)

            if user is None:
                # invalid uid
                session.pop(self.SESSION_UID)
        else:
            user = None

        return user


