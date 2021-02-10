from typing import Iterable, Optional

from pony.orm import flush

from fiar.db import User, FriendshipRequest


class FriendshipRequestRepo:
    def get_by_id(self, id: int) -> Optional[FriendshipRequest]:
        return FriendshipRequest.get(id=id)

    def get_by_users(self, sender: User, recipient: User) -> Optional[FriendshipRequest]:
        return FriendshipRequest.get(sender=sender, recipient=recipient)

    def get_all_of(self, user: User) -> Iterable[FriendshipRequest]:
        return FriendshipRequest.select(lambda r: r.sender == user or r.recipient == user)

    def get_all_sent_of(self, user: User) -> Iterable[FriendshipRequest]:
        return user.sent_friendship_requests

    def get_all_received_of(self, user: User) -> Iterable[FriendshipRequest]:
        return user.received_friendship_requests

    def create(self, sender: User, recipient: User):
        request = FriendshipRequest(sender=sender, recipient=recipient)
        flush()
        return request
