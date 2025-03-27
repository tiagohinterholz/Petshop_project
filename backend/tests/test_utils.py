from sqlalchemy import text
from backend_app import db
from backend_app.models.password_reset_model import PasswordReset
from backend_app.models.breed_model import Breed
from backend_app.models.appointment_model import Appointment
from backend_app.models.pet_model import Pet
from backend_app.models.address_model import Address        
from backend_app.models.contact_model import Contact
from backend_app.models.client_model import Client
from backend_app.models.user_model import User

def reset_test_database():
    """Remove todos os dados e reseta as sequences no banco de teste"""
    db.session.query(PasswordReset).delete()
    db.session.query(Appointment).delete()
    db.session.query(Pet).delete()                       
    db.session.query(Address).delete()                     
    db.session.query(Contact).delete()
    db.session.query(Client).delete()
    db.session.query(Breed).delete()
    db.session.query(User).delete()
    db.session.commit()

    def reset_sequence(seq_name):
        db.session.execute(text(f"ALTER SEQUENCE {seq_name} RESTART WITH 1"))

    reset_sequence("appointment_id_seq")
    reset_sequence("pet_id_seq")
    reset_sequence("address_id_seq")
    reset_sequence("contact_id_seq")
    reset_sequence("client_id_seq")
    reset_sequence("breed_id_seq")
    reset_sequence("users_id_seq")
    db.session.commit()