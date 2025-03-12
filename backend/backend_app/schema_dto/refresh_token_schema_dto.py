from marshmallow import Schema, fields

class RefreshTokenSchema(Schema):
    refresh_token = fields.String(required=True, error_messages={
        "required": "O campo refresh_token é obrigatório."
    })
