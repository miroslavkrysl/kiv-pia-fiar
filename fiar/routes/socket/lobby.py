from dependency_injector.wiring import inject, Provide
from flask_socketio import Namespace, join_room, emit

from fiar.data.models import User
from fiar.di.container import AppContainer
from fiar.persistence.sqlalchemy.repositories.invite import InviteRepo
from fiar.routes.decorators import socket_context, auth_user, RouteType

LOBBY_NAMESPACE = '/lobby'
LOBBY_ROOM = 'lobby'


class LobbySocket(Namespace):
    @socket_context()
    @auth_user(RouteType.SOCKET)
    def on_connect(self,
                   auth: User):
        join_room(auth.id)
        join_room(LOBBY_ROOM)

    @socket_context()
    @auth_user(RouteType.SOCKET)
    @inject
    def on_disconnect(self,
                      auth: User,
                      invites_repo: InviteRepo = Provide[AppContainer.invite_repo]):
        invites = invites_repo.get_all_sent_by_user(auth)

        for invite in invites:
            invites_repo.delete(invite)
            emit('invite_deleted', to=invite.recipient_id, namespace=LOBBY_NAMESPACE)
