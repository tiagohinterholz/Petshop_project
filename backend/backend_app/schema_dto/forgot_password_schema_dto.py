from marshmallow import Schema, fields

class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True, error_messages={
        "required": "O campo email é obrigatório.",
        "invalid": "Formato de email inválido."
    })