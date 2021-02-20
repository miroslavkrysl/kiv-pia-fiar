from flask import Flask

from fiar.data.repositories.user import UserRepo
from fiar.di.providers import ServiceProvider
from fiar.services.auth import AuthService
from fiar.services.hash import HashService
from fiar.services.mail import MailService
from fiar.services.pswd_token import PswdTokenService
from fiar.services.token import TokenService
from fiar.services.uid import UidService
from fiar.services.user import UserService


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
        host = app.config['MAIL']['HOST'],
        port = app.config['MAIL']['PORT'],
        username = app.config['MAIL']['USERNAME'],
        password = app.config['MAIL']['PASSWORD'],
        ssl = app.config['MAIL']['SSL'],
        tls = app.config['MAIL']['TLS'],
        sender_name = app.config['MAIL']['SENDER_NAME'],
        sender_addr = app.config['MAIL']['SENDER_ADDR'],

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


class UserServiceProvider(ServiceProvider):

    def init(self, app: Flask,
             user_repo: UserRepo,
             uid_service: UidService,
             hash_service: HashService) -> UserService:
        return UserService(user_repo, uid_service, hash_service)

    def shutdown(self, resource: UserService) -> None:
        pass
