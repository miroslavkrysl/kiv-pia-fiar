import secrets
import string
from typing import Callable


class UidService:
    """
    Creating of random unique ids.
    """

    CHARS = string.ascii_letters + string.digits

    def __init__(self, uid_length: int):
        assert uid_length >= 1
        self.uid_length = uid_length

    def make_uid(self, is_taken: Callable[[str], bool]) -> str:
        """
        Create a unique user id.
        :param is_taken: Function that checks whether the uid is already taken.
        :return: Uid string.
        """
        while True:
            uid = ''.join(secrets.choice(self.CHARS) for i in range(self.uid_length))

            if not is_taken(uid):
                return uid
