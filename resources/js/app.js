function is_online(user) {
    let last_active = new Date(user.last_active_at);
    let limit = new Date();
    limit.setSeconds(last_active.getSeconds() + $app.online_timeout);
    return limit > new Date();
}

// --- REST calls ---

function logout(success=null, error=null) {
    return $.ajax({
        url: $app.api.login.DELETE,
        type: 'delete',
        dataType: 'json',
        success: success,
        error: error
    });
}

function add_request(friend_id, success=null, error=null) {
    return $.ajax({
        url: $app.api.request.POST + friend_id,
        type: 'post',
        dataType: 'json',
        success: success,
        error: error
    });
}

function remove_request(friend_id, success=null, error=null) {
    return $.ajax({
        url: $app.api.request.DELETE + friend_id,
        type: 'delete',
        dataType: 'json',
        success: success,
        error: error
    });
}

function add_friendship(friend_id, success=null, error=null) {
    return $.ajax({
        url: $app.api.friendship.PUT + friend_id,
        type: 'put',
        dataType: 'json',
        success: success,
        error: error
    });
}

function remove_friendship(friend_id, success=null, error=null) {
    return $.ajax({
        url: $app.api.friendship.DELETE + friend_id,
        type: 'delete',
        dataType: 'json',
        success: success,
        error: error
    });
}

function get_user(id, success=null) {
    return $.getJSON($app.api.user.GET + id, null, success);
}

function get_friendships(success=null) {
    return $.getJSON($app.api.friendships.GET, null, success);
}

function get_requests(success=null) {
    return $.getJSON($app.api.requests.GET, null, success);
}

function get_online_users(success=null) {
    return $.getJSON($app.api.online_users.GET, null, success);
}

function get_invites(success=null) {
    return $.getJSON($app.api.invites.GET, null, success);
}

function get_games(success=null) {
    return $.getJSON($app.api.games.GET, null, success);
}