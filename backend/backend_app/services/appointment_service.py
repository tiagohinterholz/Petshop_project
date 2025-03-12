from backend_app.repository.appointment_repository import AppointmentRepository
from backend_app.repository.pet_repository import PetRepository

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
        
        pet = PetRepository.get_by_id(validated_data["pet_id"])
        if not pet:
            return {"error": "O pet informado não existe."}, 400
        
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
        
        pet = PetRepository.get_by_id(validated_data["pet_id"])
        if not pet:
            return {"error": "O pet informado não existe."}, 400

        try:
            updated_appointment = AppointmentRepository.update(appointment_db, validated_data)
            return updated_appointment, 200
        except Exception:
            return {"error": "Erro ao atualizar agendamento."}, 500

    @staticmethod
    def delete_appointment(id):
        """Exclui um agendamento."""
        appointment = AppointmentRepository.get_by_id(id)
        if not appointment:
            return {"error": "Agendamento não encontrado"}, 404
        
        try:
            success = AppointmentRepository.delete(appointment)
            if success:
                return {"message": "Agendamento deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir agendamento."}, 500
