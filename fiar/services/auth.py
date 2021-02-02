from flask import Flask, session, g

from fiar.db import User
from fiar.repositories.user import UserRepo


class AuthService:
    """
    Takes care of users login and logout as well as loading
    the currently logged user.

    Currently logged user is stored in g.user.

    """
    def __init__(self, app: Flask, user_repo: UserRepo):
        self.user_repo = user_repo

        app.before_request(self._load_user)

    def login(self, user: User):
        """
        Login the user.
        :param user: The user instance.
        """
        session['user_uid'] = user.uid
        self._update_user(user)

    def logout(self):
        """
        Logout the user.
        """
        if 'user_uid' in session:
            session.pop('user_uid')

    def _load_user(self):
        """
        Load the currently logged user from session.
        """
        user_uid = session.get('user_uid')

        if user_uid is not None:
            user = self.user_repo.get_by_uid(user_uid)
        else:
            user = None

        self._update_user(user)

    def _update_user(self, user: User):
        """
        Store logged user instance into the app context.
        :param user: User to be stored.
        """
        g.user = user
