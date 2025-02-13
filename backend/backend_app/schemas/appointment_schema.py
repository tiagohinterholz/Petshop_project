from backend_app import ma
from backend_app.models.appointment_model import Appointment
from marshmallow import fields

class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Appointment
        load_instance = True
        fields = ("id", "pet_id", "desc_appoint", "price", "date_appoint")
    
    pet_id = fields.Integer(required=True)
    desc_appoint = fields.String(required=True)
    price = fields.Float(required=True)
    date_appoint = fields.Date(required=True)