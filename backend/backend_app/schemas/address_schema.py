from backend_app import ma
from backend_app.models.address_model import Address, Client
from marshmallow import fields, validates, ValidationError
from backend_app import db

class AddressSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Address
        load_instance = True
        fields = ("id", "client_id", "street", "city", "neighborhood", "complement")
    
    client_id = fields.Integer(required=True)
    street = fields.String(required=True)
    city = fields.String(required=True)
    neighborhood = fields.String(required=True)
    complement = fields.String(load_default=None)
    
    @validates('client_id')
    def validate_client_id(self, value):
        existing_id = db.session.get(Client, value)
        if not existing_id:
            raise ValidationError("Cliente informado não cadastrado")
    
    @validates('client_id')
    def validate_unique_address(self, value):
        existing_address = Address.query.filter_by(client_id=value).first()
        if existing_address:
            raise ValidationError("Cliente informado já possui endereço cadastrado")