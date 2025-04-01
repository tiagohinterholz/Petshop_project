from marshmallow import Schema, fields, ValidationError, validates
from datetime import datetime

class AppointmentSchemaDTO(Schema):
    
    id = fields.Int(dump_only=True)
    pet_id = fields.Integer(required=True)
    procedure_id = fields.Integer(required=True)
    date_appoint = fields.DateTime(required=True)
        
    @validates('date_appoint')
    def validate_date_appoint(self, value):
        now = datetime.now()
        if value <= now:
            raise ValidationError("A data e hora do agendamento precisam ser futuras.")
