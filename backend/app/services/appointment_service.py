from app import db
from app.models.appointment_model import Appointment
from app.models.pet_model import Pet
from datetime import date

def register_appointment(appointment):
    pet_exists = Pet.query.get(appointment.pet_id)
    today = date.today()
    
    if not pet_exists: #tem que existir o pet
        return None
    if appointment.date_appoint < today: # a data tem que ser maior ou igual que hoje
        return None
    if appointment.price < 0: # preço não pode ser negativo
        return None
    
    appointment_db = Appointment(
        pet_id = appointment.pet_id,
        desc_appoint = appointment.desc_appoint,
        price = appointment.price,
        date_appoint = appointment.date_appoint
    )
    db.session.add(appointment_db)
    db.session.commit()
    
def list_appointments():
    return Appointment.query.all()

def list_appointment_id(id):
    return Appointment.query.filter_by(id=id).first()

def update_appointment(appointment_db, new_appointment):
    pet_exists = Pet.query.get(new_appointment.pet_id)
    if not pet_exists:
        return None
    if not appointment_db:
        return None
    appointment_db.pet_id = new_appointment.pet_id
    appointment_db.desc_appoint = new_appointment.desc_appoint
    appointment_db.price = new_appointment.price
    appointment_db.date_appoint = new_appointment.date_appoint
    
    db.session.commit()
    return appointment_db

def delete_appointment(appointment):
    if not appointment:
        return False
    db.session.delete(appointment)
    db.session.commit()
    return True
    
    