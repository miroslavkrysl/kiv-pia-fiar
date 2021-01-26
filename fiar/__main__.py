from flask_socketio import SocketIO

from fiar import di, app

if __name__ == '__main__':
    # if called as a module (python -m fiar) run socket.io web server - eventlet
    socket_io = di.injector.get(SocketIO)
    socket_io.run(app)
