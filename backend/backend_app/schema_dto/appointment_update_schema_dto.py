from marshmallow import Schema, fields, ValidationError, validates
from datetime import date

class AppointmentUpdateSchemaDTO(Schema):
    pet_id = fields.Integer(required=False)
    procedure_id = fields.Integer(required=False)
    date_appoint = fields.Date(required=False)
    
    @validates('date_appoint')
    def validate_date_appoint(self, value):
        today = date.today()   
        if value <= today: #  Data deve ser futura
            raise ValidationError("Data precisa ser maior ou igual a hoje")
    