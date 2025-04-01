from marshmallow import Schema, fields, ValidationError, validates
from datetime import date

class AppointmentSchemaDTO(Schema):
    
    id = fields.Int(dump_only=True)
    pet_id = fields.Integer(required=True)
    procedure_id = fields.Integer(required=True)
    date_appoint = fields.Date(required=True)
        
    @validates('date_appoint')
    def validate_date_appoint(self, value):
        today = date.today()   
        if value <= today: #  Data deve ser futura
            raise ValidationError("Data precisa ser maior ou igual a hoje")
