import secrets
import string

from fiar.persistence.sqlalchemy.repositories.user import UserRepo


class UidService:
    """
    Creating of random unique ids.
    """

    CHARS = string.ascii_letters + string.digits

    def __init__(self,
                 user_repo: UserRepo,
                 uid_length: int):
        assert uid_length >= 1
        self.user_repo = user_repo
        self.uid_length = uid_length

    def make_uid(self) -> str:
        """
        Create a unique user id.
        :return: Uid string.
        """
        while True:
            uid = ''.join(secrets.choice(self.CHARS) for i in range(self.uid_length))

            if self.user_repo.get_by_uid(uid) is None:
                return uid
