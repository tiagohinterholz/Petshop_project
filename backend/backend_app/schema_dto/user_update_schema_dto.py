from marshmallow import Schema, fields, validate

class UserUpdateSchemaDTO(Schema):
    email = fields.Email(required=False)  # Agora pode ser opcional
    password = fields.String(required=False, validate=validate.Length(min=6))
    name = fields.String(required=False)
