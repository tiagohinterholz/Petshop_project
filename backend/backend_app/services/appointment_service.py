from backend_app import db
from backend_app.models.appointment_model import Appointment
from backend_app.models.pet_model import Pet
from backend_app.schemas.appointment_schema import AppointmentSchema  # ✅ Adicionando a serialização correta
from datetime import date

def register_appointment(appointment_data):
    """Cadastra um novo agendamento."""
    pet_exists = Pet.query.get(appointment_data["pet_id"])
    today = date.today()

    if not pet_exists:  # ✅ O pet deve existir
        return {"error": "Pet não encontrado"}, 404  

    if appointment_data.get("date_appoint") < today:  # ✅ Data deve ser futura
        return {"error": "Data precisa ser maior ou igual a hoje"}, 400  

    if appointment_data.get("price", 0) < 0:  # ✅ Preço não pode ser negativo
        return {"error": "Preço não pode ser negativo"}, 400  

    appointment_db = Appointment(
        pet_id=appointment_data["pet_id"],
        desc_appoint=appointment_data["desc_appoint"],
        price=appointment_data["price"],
        date_appoint=appointment_data["date_appoint"]
    )

    db.session.add(appointment_db)
    db.session.commit()
    
    return AppointmentSchema().dump(appointment_db), 201

def list_appointments():
    """Lista todos os agendamentos."""
    appointments = Appointment.query.all()
    return AppointmentSchema(many=True).dump(appointments), 200 

def list_appointment_id(id):
    """Busca um agendamento pelo ID."""
    appointment = Appointment.query.get(id)
    if not appointment:
        return {"error": "Agendamento não encontrado"}, 404
    return AppointmentSchema().dump(appointment), 200  

def update_appointment(appointment_db, new_appointment_data):
    """Atualiza um agendamento."""
    if not appointment_db:
        return {"error": "Agendamento não encontrado"}, 404

    pet_exists = Pet.query.get(new_appointment_data["pet_id"])
    if not pet_exists:
        return {"error": "Pet não encontrado"}, 404  

    appointment_db.pet_id = new_appointment_data["pet_id"]
    appointment_db.desc_appoint = new_appointment_data["desc_appoint"]
    appointment_db.price = new_appointment_data["price"]
    appointment_db.date_appoint = new_appointment_data["date_appoint"]
    
    db.session.commit()
    
    return AppointmentSchema().dump(appointment_db), 200 

def delete_appointment(appointment):
    """Exclui um agendamento."""
    if not appointment:
        return {"error": "Agendamento não encontrado"}, 404  

    db.session.delete(appointment)
    db.session.commit()
    
    return {}, 204 
