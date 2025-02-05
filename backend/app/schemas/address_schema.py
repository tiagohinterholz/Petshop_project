from app import ma
from app.models.address_model import Address
from marshmallow import fields

class AddressSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Address
        load_instance = True
        fields = ("id", "client_id", "street", "city", "neighborhood", "complement")
    
    client_id = fields.Integer(required=True)
    street = fields.String(required=True)
    city = fields.String(required=True)
    neighborhood = fields.String(required=True)
    complement = fields.String(missing=None)