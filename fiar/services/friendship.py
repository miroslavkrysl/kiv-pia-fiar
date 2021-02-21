from fiar.data.models import User, Friendship
from fiar.persistence.sqlalchemy.repositories.friendship import FriendshipRepo
from fiar.persistence.sqlalchemy.repositories.request import RequestRepo


class FriendshipService:
    """
    Various friendship logic.
    """

    def __init__(self,
                 friendship_repo: FriendshipRepo,
                 request_repo: RequestRepo):
        self.friendship_repo = friendship_repo
        self.request_repo = request_repo

    def are_friends(self, user: User, friend: User):
        """
        Check whether users are friends.
        :param user: User.
        :param friend: Friend.
        :return: True if friends, False otherwise.
        """
        return self.friendship_repo.get_by_users(user, friend) is not None \
               or self.friendship_repo.get_by_users(friend, user) is not None

    def accept_friendship(self, user: User, friend: User):
        # make friendship bidirectional
        fs1 = Friendship(user.id, friend.id)
        fs2 = Friendship(friend.id, user.id)

        self.friendship_repo.add(fs1)
        self.friendship_repo.add(fs2)

        self.remove_pending_requests(user, friend)

    def deny_friendship(self, user: User, friend: User):
        # remove pending requests
        self.remove_pending_requests(user, friend)

    def remove_friendship(self, user: User, friend: User):
        # delete bidirectional friendship
        fs1 = self.friendship_repo.get_by_users(user, friend)
        fs2 = self.friendship_repo.get_by_users(friend, user)

        self.friendship_repo.delete(fs1)
        self.friendship_repo.delete(fs2)

    def is_request_pending(self, user: User, friend: User) -> bool:
        """
        Check whether there is a pending request between users.
        :param user: User.
        :param friend: Friend.
        :return: True if a request is pending, False otherwise.
        """
        return self.request_repo.get_by_users(user, friend) is not None \
               or self.request_repo.get_by_users(friend, user) is not None

    def has_received_request(self, user: User, sender: User) -> bool:
        """
        Check whether the user has received a friendship request from sender.
        :param user: User.
        :param sender: Sender.
        :return: True if a request was received, False otherwise.
        """
        return self.request_repo.get_by_users(sender, user) is not None

    def remove_pending_requests(self, user: User, friend: User):
        req1 = self.request_repo.get_by_users(user, friend)
        req2 = self.request_repo.get_by_users(friend, user)

        if req1:
            self.request_repo.delete(req1)

        if req2:
            self.request_repo.delete(req2)
