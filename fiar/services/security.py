import secrets
from typing import Optional

from flask import session, g, Flask
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from passlib.hash import bcrypt

from fiar.persistence.models import User
from fiar.persistence.repositories import UserRepository
from fiar.services.mail import MailService


class HashService:
    """
    Hashing and verifying of strings.
    """

    def hash_secret(self, secret: str) -> str:
        """
        Create a hash of given secret.
        :param secret: The secret string.
        :return: Hash string.
        """
        return bcrypt.hash(secret)

    def verify_hash(self, secret: str, hash: str) -> bool:
        """
        Verify if the hashed secret equals the given hash.
        :param secret: Secret string.
        :param hash: Hash string.
        :return: True if hashes matches, false otherwise.
        """
        return bcrypt.verify(secret, hash)


class TokenService:
    """
    Creating of signed, timed tokens from data.
    """

    def __init__(self, secret_key: str, timed_exp: int):
        self.timed_serializer = URLSafeTimedSerializer(secret_key)
        self.timed_exp = timed_exp

    def timed_token(self, data: object) -> str:
        """
        Create a token by serializing and signing given data together
        with current timestamp.
        :param data: Any object that will be serialized into the token.
        :return: String with serialized token.
        """
        return self.timed_serializer.dumps(data)

    def decode_timed_token(self, token: str) -> Optional[object]:
        """
        Deserialize data from signed timed token and check expiration time.
        :param token: The timed token.
        :return: Deserialized data or None if token is invalid or expired.
        """
        try:
            return self.timed_serializer.loads(
                token,
                max_age=self.timed_exp)
        except (BadSignature, SignatureExpired) as e:
            return None


class UidService:
    """
    Creating of random unique user ids.
    """

    def __init__(self, user_repo: UserRepository, uid_length: int):
        assert uid_length >= 32
        self.user_repo = user_repo
        self.uid_length = uid_length

    def make_uid(self) -> str:
        """
        Create a unique user id.
        :return: Uid string.
        """
        while True:
            uid = secrets.token_hex(self.uid_length // 2)

            if self.user_repo.find_by_uid(uid) is None:
                return uid


class LoginService:
    """
    Takes care of users login and logout as well as loading
    of the currently logged user.

    Currently logged user is stored in g.user.

    """
    def __init__(self, app: Flask, user_repo: UserRepository):
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
            user = self.user_repo.find_by_uid(user_uid)
        else:
            user = None

    def _update_user(self, user: User):
        """
        Store logged user instance into the app context.
        :param user: User to be stored.
        """
        g.user = user


class PasswordResetService:
    def __init__(self, mail_service: MailService, token_service: TokenService):
        self.mail_service = mail_service
        self.token_service = token_service
