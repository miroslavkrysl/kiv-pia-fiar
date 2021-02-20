from datetime import timedelta

from flask import Flask

from fiar.data.repositories.friendship import FriendshipRepo
from fiar.data.repositories.friendship_request import FriendshipRequestRepo
from fiar.data.repositories.user import UserRepo
from fiar.di.providers import ServiceProvider
from fiar.services.auth import AuthService
from fiar.services.friendship import FriendshipService
from fiar.services.hash import HashService
from fiar.services.mail import MailService
from fiar.services.pswd_token import PswdTokenService
from fiar.services.token import TokenService
from fiar.services.uid import UidService
from fiar.services.user import UserService


# --- Util services ---

class UidServiceProvider(ServiceProvider):

    def init(self, app: Flask,
             user_repo: UserRepo) -> UidService:
        uid_length = app.config['USER']['UID_LENGTH']
        return UidService(user_repo, uid_length)

    def shutdown(self, resource: UidService) -> None:
        pass


class HashServiceProvider(ServiceProvider):

    def init(self, app: Flask) -> HashService:
        return HashService()

    def shutdown(self, resource: HashService) -> None:
        pass


class TokenServiceProvider(ServiceProvider):

    def init(self, app: Flask) -> TokenService:
        key = app.config['SECRET_KEY']
        return TokenService(key)

    def shutdown(self, resource: TokenService) -> None:
        pass


class PswdTokenServiceProvider(ServiceProvider):

    def init(self, app: Flask,
             token_service: TokenService,
             user_repo: UserRepo) -> PswdTokenService:
        exp_time = app.config['USER']['PSWD_RESET_EXP']
        return PswdTokenService(token_service, user_repo, exp_time)

    def shutdown(self, resource: PswdTokenService) -> None:
        pass


class MailServiceProvider(ServiceProvider):

    def init(self, app: Flask) -> MailService:
        mail_config = app.config['MAIL']

        host = mail_config['HOST']
        port = mail_config['PORT']
        username = mail_config['USERNAME']
        password = mail_config['PASSWORD']
        ssl = mail_config['SSL']
        tls = mail_config['TLS']
        sender_name = mail_config['SENDER_NAME']
        sender_addr = mail_config['SENDER_ADDR']

        return MailService(host, port, username, password, ssl, tls, sender_name, sender_addr)

    def shutdown(self, resource: MailService) -> None:
        pass


class AuthServiceProvider(ServiceProvider):

    def init(self, app: Flask,
             user_repo: UserRepo,
             hash_service: HashService) -> AuthService:
        return AuthService(user_repo, hash_service)

    def shutdown(self, resource: AuthService) -> None:
        pass


# --- Entity services ---

class UserServiceProvider(ServiceProvider):

    def init(self, app: Flask,
             user_repo: UserRepo,
             uid_service: UidService,
             hash_service: HashService) -> UserService:
        online_timeout = timedelta(seconds=app.config['USER']['ONLINE_TIMEOUT'])
        return UserService(user_repo, uid_service, hash_service, online_timeout)

    def shutdown(self, resource: UserService) -> None:
        pass


class FriendshipServiceProvider(ServiceProvider):

    def init(self, app: Flask,
             friendship_repo: FriendshipRepo,
             friendship_request_repo: FriendshipRequestRepo) -> FriendshipService:
        return FriendshipService(friendship_repo, friendship_request_repo)

    def shutdown(self, resource: FriendshipService) -> None:
        pass
