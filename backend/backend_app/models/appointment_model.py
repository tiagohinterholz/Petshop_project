from backend_app import db
from backend_app.models.pet_model import Pet

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    desc_appoint = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    date_appoint = db.Column(db.Date, nullable=False)
    
    pet = db.relationship(Pet, backref=db.backref('appointments', lazy='dynamic'))
    