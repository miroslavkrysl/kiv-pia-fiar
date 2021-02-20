from typing import Optional

from fiar.data.models import User
from fiar.persistence.sqlalchemy.repositories.user import UserRepo
from fiar.services.token import TokenService


class PswdTokenService:
    """
    Takes care of generating and decoding password reset tokens.
    """
    def __init__(self,
                 token_service: TokenService,
                 user_repo: UserRepo,
                 exp_time: int):
        self.token_service = token_service
        self.user_repo = user_repo
        self.exp_time = exp_time

    def make_token(self, user: User) -> str:
        """
        Create a time limited password reset token for the user.
        :param user: The user.
        :return: Created token.
        """
        return self.token_service.make_token(user.uid)

    def decode_token(self, token: str) -> Optional[User]:
        """
        Decode the time limited password reset token.
        :param token: The token.
        :return: A user - owner of the token.
        """
        uid = self.token_service.decode_token(token, self.exp_time)

        if uid is not None and isinstance(uid, str):
            return self.user_repo.get_by_uid(uid)

        return None
