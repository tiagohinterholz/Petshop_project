from marshmallow import Schema, fields

class ResetPasswordSchemaDTO(Schema):
    
    token = fields.String(required=True, error_messages={
        "required": "O campo token é obrigatório."
    })
    new_password = fields.String(required=True, validate=lambda p: len(p) >= 6, error_messages={
        "required": "O campo new_password é obrigatório.",
        "invalid": "A senha deve ter no mínimo 6 caracteres."
    })
