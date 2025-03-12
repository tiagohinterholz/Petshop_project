from backend_app.repository.appointment_repository import AppointmentRepository
from backend_app.models.appointment_model import Appointment
from marshmallow import ValidationError

class AppointmentService:
    """Classe responsável pelas regras de negócio dos agendamentos."""

    @staticmethod
    def list_appointments():
        """Retorna todos os agendamentos."""
        return AppointmentRepository.list_all(), 200
        
    @staticmethod
    def list_appointment_by_id(id):
        """Retorna um agendamento pelo ID."""
        appointment = AppointmentRepository.get_by_id(id)
        if not appointment:
            return {"error": "Agendamento não encontrado"}, 404
        return appointment, 200

    @staticmethod
    def register_appointment(validated_data):
        """Cadastra um novo agendamento."""
        try:
            new_appointment = AppointmentRepository.create(validated_data)
            return new_appointment, 201
        except Exception:
            return {"error": "Erro ao cadastrar agendamento."}, 500

    @staticmethod
    def update_appointment(id, validated_data):
        """Atualiza um agendamento."""
        appointment_db = AppointmentRepository.get_by_id(id)
        if not appointment_db:
            return {"error": "Agendamento não encontrado"}, 404

        try:
            updated_appointment = AppointmentRepository.update(appointment_db, validated_data)
            return {
                "id": updated_appointment.id,
                "pet_id": updated_appointment.pet_id,
                "desc_appoint": updated_appointment.desc_appoint,
                "price": updated_appointment.price,
                "date_appoint": str(updated_appointment.date_appoint)
            }, 200
        except Exception:
            return {"error": "Erro ao atualizar agendamento."}, 500

    @staticmethod
    def delete_appointment(id):
        """Exclui um agendamento."""
        appointment = AppointmentRepository.get_by_id(id)
        if not appointment:
            return {"error": "Agendamento não encontrado"}, 404
        
        try:
            AppointmentRepository.delete(appointment)
            return {"message": "Agendamento deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir agendamento."}, 500
