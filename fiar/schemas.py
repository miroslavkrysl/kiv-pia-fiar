from marshmallow import Schema, fields, validate, pre_load, post_dump


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=[
        lambda x: x.isprintable(),
        validate.Length(min=3, max=32)
    ])
    email = fields.Email(required=True, validate=[
        validate.Length(max=255)
    ])
    password = fields.Str(required=True, load_only=True)
    is_admin = fields.Boolean(required=True, dump_only=True)
    last_active_at = fields.DateTime(dump_only=True)
    uid = fields.Str(dump_only=True)

    # @pre_load
    # def process_input(self, data, **kwargs):
    #     data["email"] = data["email"].lower().strip()
    #     return data

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "users" if many else "user"
        return {key: data}


user_schema = UserSchema()
user_login_schema = UserSchema(only=[
        'email',
        'password'
])
