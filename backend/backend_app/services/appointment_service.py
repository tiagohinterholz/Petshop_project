from backend_app import db
from backend_app.models.appointment_model import Appointment
from backend_app.schemas.appointment_schema import AppointmentSchema
from marshmallow import ValidationError


def list_appointments():
    """Lista todos os agendamentos."""
    try:
        appointments = Appointment.query.all()
        return AppointmentSchema(many=True).dump(appointments), 200 
    except Exception as e:
        return {"error": f"Erro ao listar agendamentos: {e}"}, 500
    
def register_appointment(appointment_data):
    """Cadastra um novo agendamento."""
 
    schema = AppointmentSchema()
    
    try:
        validated_data = schema.load(appointment_data)
    except ValidationError as err:
        return {"error": err.messages}, 400
        

    appointment_db = Appointment(
        pet_id=validated_data["pet_id"],
        desc_appoint=validated_data["desc_appoint"],
        price=validated_data["price"],
        date_appoint=validated_data["date_appoint"]
    )
    try:
        db.session.add(appointment_db)
        db.session.commit()
        return schema.dump(appointment_db), 201
    except Exception as e:
        return {"error": f"Erro ao cadastrar agendamento."}, 500

def list_appointment_id(id):
    """Busca um agendamento pelo ID."""
    
    try:
        appointment = db.session.get(Appointment, id)
        if not appointment:
            return {"error": "Agendamento não encontrado"}, 404
        return AppointmentSchema().dump(appointment), 200
    except Exception as e:
        return {"error": f"Erro ao buscar agendamento: {str(e)}"}, 500  

def update_appointment(appointment_db, new_appointment_data):
    """Atualiza um agendamento."""
    if not appointment_db:
        return {"error": "Agendamento não encontrado"}, 404
    
    try:
        appointment_db.pet_id = new_appointment_data["pet_id"]
        appointment_db.desc_appoint = new_appointment_data["desc_appoint"]
        appointment_db.price = new_appointment_data["price"]
        appointment_db.date_appoint = new_appointment_data["date_appoint"]
        
        db.session.commit()  
        return AppointmentSchema().dump(appointment_db), 200 
    except Exception as e:
        return {"error": f"Erro ao atualizar agendamento: {str(e)}"}, 500 
        
def delete_appointment(id):
    """Exclui um agendamento."""
    try:
        appointment = db.session.get(Appointment, id)
        if not appointment:
            return {"error": "Agendamento não encontrado"}, 404  
        db.session.delete(appointment)
        db.session.commit()
        return {"message": "Agendamento deletado com sucesso"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao excluir agendamento: {str(e)}"}, 500

