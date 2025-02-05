from app import ma, db
from app.models.contact_model import Contact, ContactTypeEnum
from marshmallow import fields

class ContactSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Contact
        load_instance = True
        fields = ("id", "client_id", "type_contact", "value_contact")
        sqla_session = db.session
    
    client_id = fields.Integer(required=True)
    type_contact = fields.Enum(ContactTypeEnum, by_value=True, required=True)
    value_contact = fields.String(required=True)