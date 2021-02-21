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

function add_invite(opponent_id, success=null, error=null) {
    return $.ajax({
        url: $app.api.invite.POST + opponent_id,
        type: 'post',
        dataType: 'json',
        success: success,
        error: error
    });
}

function remove_invite(opponent_id, success=null, error=null) {
    return $.ajax({
        url: $app.api.invite.DELETE + opponent_id,
        type: 'delete',
        dataType: 'json',
        success: success,
        error: error
    });
}

function accept_invite(friend_id, success=null, error=null) {
    return $.ajax({
        url: $app.api.game.POST + friend_id,
        type: 'put',
        dataType: 'json',
        success: success,
        error: error
    });
}

function refuse_invite(friend_id, success=null, error=null) {
    return $.ajax({
        url: $app.api.invite.DELETE + friend_id,
        type: 'delete',
        dataType: 'json',
        success: success,
        error: error
    });
}