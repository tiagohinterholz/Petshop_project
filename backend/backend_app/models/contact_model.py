from backend_app import db
from backend_app.models.client_model import Client
from sqlalchemy import Enum
class Contact(db.Model):
    __tablename__= 'contact'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    type_contact = db.Column(Enum("telefone", "email", name="contact_type_enum"), nullable=False)
    value_contact = db.Column(db.String(100), nullable=False)
    
    client = db.relationship(Client, backref=db.backref('contacts', lazy='dynamic'))
    