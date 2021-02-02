from typing import Optional

from flask import session, g, Flask

from fiar.db import User
from fiar.repositories.user import UserRepo
from fiar.services.hash import HashService


class AuthService:
    """
    Takes care of authenticating users, login and logout within the session
    as well as loading the currently logged user from the session.
    """

    SESSION_UID_NAME = 'user_uid'
    G_VAR_NAME = 'auth'
    G_USER_NAME = 'user'

    def __init__(self, app: Flask, user_repo: UserRepo, hash_service: HashService):
        self.user_repo = user_repo
        self.hash_service = hash_service

        app.before_request(self._before_request)

    def auth_email_password(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate the user.
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
        session[self.SESSION_UID_NAME] = user.uid
        self._set_user(user)

    def logout(self):
        """
        Logout the user from the session.
        """
        if self.SESSION_UID_NAME in session:
            session.pop(self.SESSION_UID_NAME)

        self._set_user(None)

    def get_user(self) -> Optional[User]:
        """
        Get the currently logged user from the session.
        """
        return self._get_user()

    def _before_request(self):
        print('useeeer')
        # setup auth global var
        setattr(g, self.G_VAR_NAME, {})

        # load user
        user_uid = session.get(self.SESSION_UID_NAME)

        if user_uid is not None:
            user = self.user_repo.get_by_uid(user_uid)

            if user is None:
                # invalid uid
                session.pop(self.SESSION_UID_NAME)
        else:
            user = None

        self._set_user(user)

    def _set_user(self, user: Optional[User]):
        getattr(g, self.G_VAR_NAME)[self.G_USER_NAME] = user

    def _get_user(self) -> User:
        return getattr(g, self.G_VAR_NAME)[self.G_USER_NAME]
