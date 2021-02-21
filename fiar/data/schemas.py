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
    is_admin = fields.Boolean()
    last_active_at = fields.DateTime()

    @post_load
    def process_input(self, data, **kwargs):
        # preprocess email
        if "email" in data:
            data["email"] = data["email"].lower().strip()
        return data


user_schema = UserSchema()


# --- Game ---

class GameSchema(Schema):
    id = fields.Int(dump_only=True)
    player_o_id = fields.Int(required=True)
    player_x_id = fields.Int(required=True)
    winner = fields.Int(allow_none=True)
    created_at = fields.DateTime()
    ended_at: fields.DateTime(allow_none=True)


game_schema = GameSchema()


# --- Move ---

class MoveSchema(Schema):
    side = fields.Int(required=True, validate=[
        validate.OneOf([0, 1])
    ])
    row = fields.Int(required=True)
    col = fields.Int(required=True)


move_schema = GameSchema()
