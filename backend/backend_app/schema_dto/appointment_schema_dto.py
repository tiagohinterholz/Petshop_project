from marshmallow import Schema, fields, ValidationError, validates
from datetime import date

class AppointmentSchemaDTO(Schema):
    
    id = fields.Int(dump_only=True)
    pet_id = fields.Integer(required=True)
    desc_appoint = fields.String(required=True)
    price = fields.Float(required=True)
    date_appoint = fields.Date(required=True)

    @validates('price')
    def validate_price(self, value):
        if value < 0:  # Preço não pode ser negativo
            raise ValidationError("Preço do atendimento não pode ser negativo. Informe valor válido.")
        
    @validates('date_appoint')
    def validate_date_appoint(self, value):
        today = date.today()   
        if value <= today: #  Data deve ser futura
            raise ValidationError("Data precisa ser maior ou igual a hoje")
    
    @validates('desc_appoint')
    def validate_desc_appoint(self, value):
        if not value.strip():  # Remove espaços e verifica se está vazio
            raise ValidationError("A descrição do atendimento não pode estar vazia.")