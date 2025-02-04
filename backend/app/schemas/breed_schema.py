from app import ma
from app.models.breed_model import Breed
from marshmallow import fields

class BreedSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Breed
        load_instance = True
        fields = ('id', 'description')
    
    description = fields.String(required=True)