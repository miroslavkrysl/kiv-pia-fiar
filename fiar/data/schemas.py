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
