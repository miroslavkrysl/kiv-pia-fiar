from datetime import timedelta

from flask import Flask

from fiar.persistence.sqlalchemy.repositories.friendship import FriendshipRepo
from fiar.persistence.sqlalchemy.repositories.game import GameRepo
from fiar.persistence.sqlalchemy.repositories.invite import InviteRepo
from fiar.persistence.sqlalchemy.repositories.move import MoveRepo
from fiar.persistence.sqlalchemy.repositories.request import RequestRepo
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.di.providers import ServiceProvider
from fiar.services.auth import AuthService
from fiar.services.friendship import FriendshipService
from fiar.services.game import GameService
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
             friendship_request_repo: RequestRepo) -> FriendshipService:
        return FriendshipService(friendship_repo, friendship_request_repo)

    def shutdown(self, resource: FriendshipService) -> None:
        pass


class GameServiceProvider(ServiceProvider):

    def init(self, app: Flask,
             game_repo: GameRepo,
             invite_repo: InviteRepo,
             move_repo: MoveRepo) -> GameService:
        board_size = app.config['GAME']['BOARD_SIZE']
        return GameService(game_repo, invite_repo, move_repo, board_size)

    def shutdown(self, resource: GameService) -> None:
        pass
