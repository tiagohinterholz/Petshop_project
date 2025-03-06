from backend_app import ma, db
from backend_app.models.contact_model import Contact, Client
from marshmallow import fields, validates, ValidationError, pre_load

class ContactSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Contact
        load_instance = True
        fields = ("id", "client_id", "type_contact", "value_contact")
        sqla_session = db.session
    
    client_id = fields.Integer(required=True)
    type_contact = fields.Str(required=True)
    value_contact = fields.String(required=True)
    
    @validates('client_id')
    def validate_client_id(self, value):
        existing_id = db.session.get(Client, value)
        if not existing_id:
            raise ValidationError("Cliente informado não cadastrado")
