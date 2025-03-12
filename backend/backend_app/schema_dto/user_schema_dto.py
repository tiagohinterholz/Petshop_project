from marshmallow import Schema, fields
from backend_app.models.user_model import ProfileEnum

class UserSchemaDTO(Schema):
    
    cpf = fields.String(required=True, metadata={"unique": True})
    name = fields.String(required=True)
    profile = fields.Enum(ProfileEnum, by_value=True, required=True)
    password = fields.String(required=True, load_only=True)