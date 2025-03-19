from marshmallow import Schema, fields, validates, ValidationError
import re

class LoginSchemaDTO(Schema):
    cpf = fields.String(required=True)
    password = fields.String(required=True)
    
    @validates("cpf")
    def validate_cpf(self, value):
        """Valida se o CPF está no formato 000.000.000-00"""
        if not re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", value):
            raise ValidationError("CPF deve estar no formato 000.000.000-00.")
    
    @validates('password')
    def validate_password(self, value):
        """Valida se a senha tem pelo menos 6 caracteres."""
        if len(value) < 6:
            raise ValidationError("A senha deve ter no mínimo 6 caracteres")
    
    @classmethod
    def validate_login(cls, data):
        """Valida os dados de login antes de passar para o service."""
        schema = cls()
        errors = schema.validate(data)
        if errors:
            return {"error": errors}, 400
        return None