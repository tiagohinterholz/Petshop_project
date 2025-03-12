from backend_app import ma, db 
from backend_app.models.pet_model import Pet, Client, Breed
from marshmallow import fields, validates, ValidationError

class PetRepository(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Pet
        load_instance = True
        fields = ("id", "client_id", "breed_id", "birth_date", "name")

    client_id = fields.Integer(required=True)
    breed_id = fields.Integer(required=True)
    birth_date = fields.Date(required=True)
    name = fields.String(required=True)

    @validates('client_id')
    def validate_client_id(self, value):
        existing_id = db.session.get(Client, value)
        if not existing_id:
            raise ValidationError("Cliente informado não cadastrado")
    @validates('breed_id')
    def validate_breed_id(self, value):
        existing_id = db.session.get(Breed, value)
        if not existing_id:
            raise ValidationError("Raça informada não cadastrada")