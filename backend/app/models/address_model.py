from backend import db
from app.models.client_model import Client

class Address(db.Model):
    __tablename__= 'address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    neighborhood = db.Column(db.String(50), nullable=False)
    complement = db.Column(db.String(50), nullable=True)

    client = db.relationship(Client, backref=db.backref('addresses', lazy='dynamic'))