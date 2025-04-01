from marshmallow import Schema, fields, ValidationError, validates
from datetime import datetime

class AppointmentUpdateSchemaDTO(Schema):
    pet_id = fields.Integer(required=False)
    procedure_id = fields.Integer(required=False)
    date_appoint = fields.DateTime(required=False)
    
    @validates('date_appoint')
    def validate_date_appoint(self, value):
        now = datetime.now()
        if value <= now:
            raise ValidationError("A data e hora do agendamento precisam ser futuras.")
    