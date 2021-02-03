# from datetime import datetime, timedelta
# from typing import List
#
# from sqlalchemy import and_, or_
#
# from fiar.persistence.db import Database
# from fiar.persistence.models import User, Friendship, FriendshipRequest
#
#
# class UserDao:
#
#     def __init__(self, db: Database):
#         self.db = db
#
#     def find_all(self) -> List[User]:
#         return self.db.session \
#             .query(User) \
#             .all()
#
#     def find_all_online(self, online_expiration: timedelta) -> List[User]:
#         now = datetime.now()
#         expiration_at = now - online_expiration
#
#         return self.db.session \
#             .query(User) \
#             .filter(User.last_active_at > expiration_at) \
#             .all()
#
#     def find_by_uid(self, uid: str):
#         return self.db.session.query(User) \
#             .filter_by(uid=uid) \
#             .first()
#
#     def find_by_email(self, uid: str):
#         return self.db.session.query(User) \
#             .filter_by(uid=uid) \
#             .first()
#
#     def save(self, user: User):
#         self.db.session.add(user)
#         self.db.session.commit()
#
#     def delete_all(self):
#         self.db.session.query(User).delete()


# class FriendshipRepository:
#     def __init__(self, db: Database):
#         self.db = db
#
#     def find_all_friends_of(self, user: User) -> List[User]:
#         friendships = self.db.session \
#             .query(Friendship) \
#             .filter(Friendship.from_user_id == user.id) \
#             .all()
#
#         return list(map(lambda f: f.to_user, friendships))
#
#     def find_all_requests_from(self, user: User) -> List[User]:
#         request = self.db.session \
#             .query(FriendshipRequest) \
#             .filter(FriendshipRequest.from_user_id == user.id) \
#             .all()
#
#         return list(map(lambda f: f.to_user, request))
#
#     def find_all_requests_to(self, user: User) -> List[FriendshipRequest]:
#         requests = self.db.session \
#             .query(FriendshipRequest) \
#             .filter(FriendshipRequest.to_user_id == user.id) \
#             .all()
#
#         return list(map(lambda f: f.from_user, requests))
#
#     def add_friendship(self, user: User, friend: User):
#         self.db.session.save(Friendship(user.id, friend.id))
#         self.db.session.save(Friendship(friend.id, user.id))
#         self.db.session.commit()
#
#     def add_request(self, from_user: User, to_user: User):
#         self.db.session.save(FriendshipRequest(from_user.id, to_user.id))
#         self.db.session.commit()
#
#     def delete_friendship(self, user: User, friend: User):
#         self.db.session \
#             .query(Friendship) \
#             .filter(
#             or_(
#                 and_(Friendship.from_user_id == user.id, Friendship.to_user_id == friend.id),
#                 and_(Friendship.from_user_id == friend.id, Friendship.to_user_id == user.id)
#             )) \
#             .delete()
#         self.db.session.commit()
#
#     def delete_request(self, request: FriendshipRequest):
#         self.db.session.delete(request)
#         self.db.session.commit()
