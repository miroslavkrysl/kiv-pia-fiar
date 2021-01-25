from flask_socketio import SocketIO

from . import app, di

if __name__ == '__main__':
    socket_io = di.get(SocketIO)
    socket_io.run(app)
