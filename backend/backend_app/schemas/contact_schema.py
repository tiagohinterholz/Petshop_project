from backend_app import ma, db
from backend_app.models.contact_model import Contact, ContactTypeEnum
from marshmallow import fields

class ContactSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Contact
        load_instance = True
        fields = ("id", "client_id", "type_contact", "value_contact")
        sqla_session = db.session
    
    client_id = fields.Integer(required=True)
    type_contact = fields.Method("serialize_enum", deserialize="deserialize_enum")
    value_contact = fields.String(required=True)

    def serialize_enum(self, obj):
        """Converte ENUM para string na saída"""
        if isinstance(obj, dict):  
            return obj["type_contact"]  #  Se for dicionário
        return obj.type_contact.value  #  Se for objeto SQLAlchemy

    def deserialize_enum(self, value):
        """Converte string para ENUM ao carregar os dados"""
        return ContactTypeEnum(value)  # Converte String → ENUM
