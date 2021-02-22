from marshmallow import Schema, fields, validate, pre_load, post_dump, post_load


# --- User ---

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=[
        lambda x: x.isprintable(),
        validate.Length(min=3, max=16)
    ])
    email = fields.Email(required=True, validate=[
        validate.Length(max=255)
    ])
    password = fields.Str(required=True, load_only=True)
    is_admin = fields.Boolean(dump_only=True)
    last_active_at = fields.DateTime(dump_only=True)

    @post_load
    def process_input(self, data, **kwargs):
        # preprocess email
        if "email" in data:
            data["email"] = data["email"].lower().strip()
        return data


user_schema = UserSchema()


# --- Friendship ---

class FriendshipSchema(Schema):
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)


friendship_schema = FriendshipSchema()


# --- Request ---

class RequestSchema(Schema):
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)


request_schema = RequestSchema()


# --- Invite ---

class InviteSchema(Schema):
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)


invite_schema = InviteSchema()


# --- Game ---

class GameSchema(Schema):
    id = fields.Int(dump_only=True)
    player_o_id = fields.Int(required=True)
    player_x_id = fields.Int(required=True)
    winner = fields.Int(allow_none=True)
    on_turn = fields.Int(allow_none=True)


game_schema = GameSchema()


# --- Move ---

class MoveSchema(Schema):
    row = fields.Int(required=True)
    col = fields.Int(required=True)


move_schema = MoveSchema()


# --- Board ---

class BoardMoveSchema:
    side = fields.Int(required=True)
    row = fields.Int(required=True)
    col = fields.Int(required=True)


board_schema = BoardMoveSchema()


# --- Admin ---

class AdminSchema(Schema):
    is_admin = fields.Boolean()


admin_schema = AdminSchema()
