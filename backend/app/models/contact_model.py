from app import db
from app.models.client_model import Client
import enum

class ContactTypeEnum(enum.Enum):
    TELEFONE = 'telefone'
    EMAIL = 'email'

class Contact(db.Model):
    __tablename__= 'contact'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    type_contact = db.Column(db.Enum(ContactTypeEnum, name='contact_type_enum'), nullable=False)
    value_contact = db.Column(db.String(100), nullable=False)
    
    client = db.relationship(Client, backref=db.backref('contacts', lazy='dynamic'))