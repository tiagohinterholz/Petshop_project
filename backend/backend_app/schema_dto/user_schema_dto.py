from marshmallow import Schema, fields, validates, ValidationError
from backend_app.models.user_model import ProfileEnum
import re

class UserSchemaDTO(Schema):
    
    cpf = fields.String(required=True)
    name = fields.String(required=True)
    profile = fields.Enum(ProfileEnum, by_value=True, required=True)
    password = fields.String(required=True, load_only=True)
    email = fields.Email(required=True)
    
    @validates('cpf')
    def validate_cpf(self, value):
        """Valida o formato do CPF (XXX.XXX.XXX-XX)."""
        pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
        if not re.match(pattern, value):
            raise ValidationError("CPF deve estar no formato XXX.XXX.XXX-XX")