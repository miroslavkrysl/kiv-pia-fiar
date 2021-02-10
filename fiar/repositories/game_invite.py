from typing import Iterable

from pony.orm import flush

from fiar.db import User, FriendshipRequest, GameInvite


class GameInviteRepo:
    def __init__(self):
        pass

    def get_all_of(self, user: User) -> Iterable[FriendshipRequest]:
        return FriendshipRequest.select(lambda r: r.sender == user or r.recipient == user)

    def get_by_id(self, id: int) -> FriendshipRequest:
        return GameInvite.get(id=id)

    def get_all_sent_of(self, user: User) -> Iterable[GameInvite]:
        return user.sent_game_invites

    def get_all_received_of(self, user: User) -> Iterable[GameInvite]:
        return user.received_game_invites

    def create(self, sender: User, recipient: User):
        invite = GameInvite(sender=sender, recipient=recipient)
        flush()
        return invite


