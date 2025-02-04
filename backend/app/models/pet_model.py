from backend import db
from backend.models.breed_model import Breed
from backend.models.client_model import Client

class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    breed_id = db.Column(db.Integer, db.ForeignKey('breed.id'), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    
    breed = db.relationship('Breed', backref=db.backref('pets', lazy='dynamic'))
    client = db.relationship('Client', backref=db.backref('pets', lazy='dynamic'))
    
    