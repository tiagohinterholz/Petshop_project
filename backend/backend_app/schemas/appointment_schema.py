from backend_app import ma, db
from backend_app.models.appointment_model import Appointment, Pet
from marshmallow import fields, validates, ValidationError
from datetime import date

class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Appointment
        load_instance = True
        fields = ("id", "pet_id", "desc_appoint", "price", "date_appoint")
    
    pet_id = fields.Integer(required=True)
    desc_appoint = fields.String(required=True)
    price = fields.Float(required=True)
    date_appoint = fields.Date(required=True)
    
    @validates('pet_id')
    def validate_pet_id(self, value):
        existing_id = db.session.get(Pet, value)
        if not existing_id:
            raise ValidationError("Pet informado não cadastrado")
        
    @validates('price')
    def validate_price(self, value):
        if value < 0:  # Preço não pode ser negativo
            raise ValidationError("Preço não pode ser negativo")
    

    @validates('date_appoint')
    def validate_date_appoint(self, value):
        today = date.today()   
        if value < today: #  Data deve ser futura
            raise ValidationError("Data precisa ser maior ou igual a hoje") 