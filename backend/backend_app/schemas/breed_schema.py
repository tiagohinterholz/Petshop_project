from backend_app import ma
from backend_app.models.breed_model import Breed
from marshmallow import fields, validates, ValidationError
from backend_app import db

class BreedSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Breed
        load_instance = True
        fields = ('id', 'description')
    
    description = fields.String(required=True)
    
    @validates('description')
    def description_validate(self, value):
        """Verifica se a raça já está cadastrada."""
        exists_breed = Breed.query.filter_by(description=value).first()
        if exists_breed:
            raise ValidationError("Raça já cadastrada")