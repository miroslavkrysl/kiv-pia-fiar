from typing import Iterable

from fiar.data.models import User, Friendship
from fiar.data.repositories.friendship import FriendshipRepo
from fiar.data.repositories.friendship_request import FriendshipRequestRepo


class FriendshipService:
    """
    Various friendship logic.
    """

    def __init__(self,
                 friendship_repo: FriendshipRepo,
                 friendship_request_repo: FriendshipRequestRepo):
        self.friendship_repo = friendship_repo
        self.friendship_request_repo = friendship_request_repo

    def are_friends(self, user: User, friend: User):
        """
        Check whether users are friends.
        :param user: User.
        :param friend: Friend.
        :return: True if friends, False otherwise.
        """
        return self.friendship_repo.get_by_users(user, friend) is not None \
               or self.friendship_repo.get_by_users(friend, user) is not None

    def make_friendship(self, user: User, friend: User):
        # make friendship bidirectional
        fs1 = Friendship(user.id, friend.id)
        fs2 = Friendship(friend.id, user.id)

        self.friendship_repo.add(fs1)
        self.friendship_repo.add(fs2)

        # remove pending requests
        fs_req1 = self.friendship_request_repo.get_by_users(user, friend)
        fs_req2 = self.friendship_request_repo.get_by_users(friend, user)

        if fs_req1:
            self.friendship_request_repo.delete(fs_req1)

        if fs_req2:
            self.friendship_request_repo.delete(fs_req2)

    def remove_friendship(self, user: User, friend: User):
        # delete bidirectional friendship
        fs1 = self.friendship_repo.get_by_users(user, friend)
        fs2 = self.friendship_repo.get_by_users(friend, user)

        self.friendship_repo.delete(fs1)
        self.friendship_repo.delete(fs2)

    def is_request_pending(self, user: User, friend: User):
        """
        Check whether users are friends.
        :param user: User.
        :param friend: Friend.
        :return: True if friends, False otherwise.
        """
        return self.friendship_request_repo.get_by_users(user, friend) is not None \
               or self.friendship_request_repo.get_by_users(friend, user) is not None

