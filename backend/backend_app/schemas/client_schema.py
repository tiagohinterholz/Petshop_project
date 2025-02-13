from backend_app import ma
from backend_app.models.client_model import Client
from marshmallow import fields

class ClientSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Client
        load_instance = True
        fields = ("id", "name", "cpf", "register_date")
    
    name = fields.String(required=True)
    cpf = fields.String(required=True)
    register_date = fields.Date(required=True)