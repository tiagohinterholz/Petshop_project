from marshmallow import Schema, fields, validates, ValidationError

class ProcedureUpdateSchemaDTO(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=False)
    description = fields.String(required=False)
    price = fields.Float(required=False)
    time_service = fields.Integer(required=False)  # minutos
    
    @validates('price')
    def validate_price(self, value):
        if value < 0:  # Preço não pode ser negativo
            raise ValidationError("Preço do atendimento não pode ser negativo. Informe valor válido.")
    
    @validates('description')
    def validate_description(self, value):
        if not value.strip():  # Remove espaços e verifica se está vazio
            raise ValidationError("A descrição do atendimento não pode estar vazia.")
