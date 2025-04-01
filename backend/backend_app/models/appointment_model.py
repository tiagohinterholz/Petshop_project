from backend_app import db
from backend_app.models.pet_model import Pet
from backend_app.models.procedure_model import Procedure
from datetime import datetime, date
class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure.id'), nullable=False)
    date_appoint = db.Column(db.DateTime, nullable=False)
    
    pet = db.relationship(Pet, backref=db.backref('appointments', lazy='dynamic'))
    procedure = db.relationship(Procedure, backref=db.backref('appointments', lazy='dynamic'))
