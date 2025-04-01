from marshmallow import Schema, fields, validates, ValidationError

class ProcedureSchemaDTO(Schema):
    id = fields.Int(dump_only=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)
    time_service = fields.Integer(required=True)  # minutos
    
    @validates('price')
    def validate_price(self, value):
        if value < 0:  # Preço não pode ser negativo
            raise ValidationError("Preço do atendimento não pode ser negativo. Informe valor válido.")
    
    @validates('description')
    def validate_description(self, value):
        if not value.strip():  # Remove espaços e verifica se está vazio
            raise ValidationError("A descrição do atendimento não pode estar vazia.")