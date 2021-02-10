from typing import Iterable, Optional

from fiar.db import User, Friendship


class FriendshipRepo:
    def __init__(self):
        pass

    def get_by_id(self, id: int) -> Optional[Friendship]:
        return Friendship.get(id=id)

    def get_by_users(self, sender: User, recipient: User) -> Optional[Friendship]:
        return Friendship.get(sender=sender, recipient=recipient)

    def get_all_of(self, user: User) -> Iterable[Friendship]:
        return user.sent_friendships

    def create(self, user: User, friend: User):
        fs = Friendship(sender=user, recipient=friend)
        Friendship(sender=friend, recipient=user)
        return fs
