from backend_app import db
from backend_app.models.appointment_model import Appointment

class AppointmentRepository:

    @staticmethod
    def list_all():
        """Lista todos os agendamentos."""
        return Appointment.query.all()
    
    @staticmethod
    def list_all_interval_time(t1, t2):
        """Lista todos os agendamentos entre o intervalo T1 e T2."""
        return Appointment.query.filter(
            Appointment.date_appoint >= t1,
            Appointment.date_appoint <= t2
        ).all()
    
    @staticmethod
    def get_by_id(id):
        """Busca um agendamento pelo ID."""
        return db.session.get(Appointment, id)
    
    @staticmethod
    def get_by_pet_id(pet_id):
        """Busca todos appointments pelo PET ID."""
        return db.session.query(Appointment).filter_by(pet_id=pet_id).all()

    @staticmethod
    def create(validated_data):
        """Cria um novo agendamento."""
        new_appointment = Appointment(
            pet_id=validated_data["pet_id"],
            procedure_id=validated_data["procedure_id"],
            date_appoint=validated_data["date_appoint"]
            )
        db.session.add(new_appointment)
        db.session.commit()
        db.session.refresh(new_appointment)
        return new_appointment

    @staticmethod
    def update(appointment, new_data):
        """Atualiza um agendamento no banco de dados."""
        appointment.pet_id = new_data.get("pet_id", appointment.pet_id)
        appointment.procedure_id = new_data.get("procedure_id", appointment.procedure_id)
        appointment.date_appoint = new_data.get("date_appoint", appointment.date_appoint)
        db.session.commit()
        return appointment

    @staticmethod
    def delete(appointment):
        """Exclui um agendamento."""
        db.session.delete(appointment)
        db.session.commit()
        return True