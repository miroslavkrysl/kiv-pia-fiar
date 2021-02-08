let user_socket;
let active_beat;

$(document).ready(function () {
    user_socket = io('/user');

    user_socket.on('connect', function () {
        active_beat = setInterval(function () {
            user_socket.emit('active', {});
        }, 1000);
    });

    user_socket.on('logout', function () {
        user_socket.disconnect();
        $(location).attr('href', '/');
    });
});