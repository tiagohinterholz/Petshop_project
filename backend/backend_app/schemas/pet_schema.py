from backend_app import ma 
from backend_app.models.pet_model import Pet
from marshmallow import fields

class PetSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Pet
        load_instance = True
        fields = ("id", "client_id", "breed_id", "birth_date", "name")
        
    client_id = fields.Integer(required=True)
    breed_id = fields.Integer(required=True)
    birth_date = fields.Date(required=True)
    name = fields.String(required=True)