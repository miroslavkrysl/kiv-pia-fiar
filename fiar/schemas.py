from marshmallow import Schema, fields, validate, pre_load, post_dump, post_load


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
    is_admin = fields.Boolean(required=True, dump_only=True)
    last_active_at = fields.DateTime(dump_only=True)

    @post_load
    def process_input(self, data, **kwargs):
        if "email" in data:
            data["email"] = data["email"].lower().strip()
        return data


user_schema = UserSchema()

user_login_schema = UserSchema(only=[
    'email',
    'password'
])

user_password_schema = UserSchema(only=[
    'password'
])

user_email_schema = UserSchema(only=[
    'email'
])


class IdSchema(Schema):
    id = fields.Int()


id_schema = IdSchema()
