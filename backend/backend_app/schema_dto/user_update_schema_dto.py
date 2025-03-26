from marshmallow import Schema, fields, validate
from backend_app.models.user_model import ProfileEnum

class UserUpdateSchemaDTO(Schema):
    cpf = fields.String(required=False)
    name = fields.String(required=False)
    email = fields.Email(required=False)  # Agora pode ser opcional
    profile = fields.Enum(ProfileEnum, by_value=True, required=True)
    password = fields.String(required=False, validate=validate.Length(min=6))
    
