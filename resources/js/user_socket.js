let user_socket;

$(document).ready(function () {
    user_socket = io('/user');

    user_socket.on('connect', function () {
        setInterval(function () {
            user_socket.emit('active', {});
        }, 1000);
    });

    user_socket.on('logout', function () {
        user_socket.disconnect();
        $(location).attr('href', '/');
    });
});