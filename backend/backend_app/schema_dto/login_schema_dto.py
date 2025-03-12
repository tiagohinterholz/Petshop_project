from marshmallow import Schema, fields, validates, ValidationError
import re

class LoginSchema(Schema):
    cpf = fields.String(required=True)
    password = fields.String(required=True)
    
    @validates('cpf')
    def validate_cpf(self, value):
        """Valida se o CPF tem exatamente 11 dígitos numéricos."""
        if not re.fullmatch(r"\d{11}", value):
            raise ValidationError("CPF deve conter exatamente 11 dígitos numéricos.")
    
    @validates('password')
    def validate_password(self, value):
        """Valida se a senha tem pelo menos 6 caracteres."""
        if len(value) < 6:
            raise ValidationError("A senah deve ter no mínimo 6 caracteres")
    
    @classmethod
    def validate_login(cls, data):
        """Valida os dados de login antes de passar para o service."""
        schema = cls()
        errors = schema.validate(data)
        if errors:
            return {"error": errors}, 400
        return None