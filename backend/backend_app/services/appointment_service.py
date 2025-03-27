from backend_app.repository.appointment_repository import AppointmentRepository
from backend_app.repository.pet_repository import PetRepository
from backend_app.schema_dto.appointment_schema_dto import AppointmentSchemaDTO
class AppointmentService:
    """Classe responsável pelas regras de negócio dos agendamentos."""
    def list_appointments():
        """Retorna todos os agendamentos."""
        appoints = AppointmentRepository.list_all()
        return AppointmentSchemaDTO(many=True).dump(appoints), 200     

    def list_appointment_id(id):
        """Retorna um agendamento pelo ID."""
        
        appointment = AppointmentRepository.get_by_id(id)
        if not appointment:
            return {"error": "Agendamento não encontrado"}, 404
        return AppointmentSchemaDTO().dump(appointment), 200

    def list_appointment_pet_id(pet_id):
        """Retorna um aagendamento pelo pet ID."""
        appointments = AppointmentRepository.get_by_pet_id(pet_id)
        if not appointments:
            return [], 200
        return AppointmentSchemaDTO(many=True).dump(appointments), 200

    def register(validated_data):
        """Cadastra um novo agendamento."""
        
        pet = PetRepository.get_by_id(validated_data["pet_id"])
        if not pet:
            return {"error": "Pet informado não existe."}, 404
        
        try:
            new_appointment = AppointmentRepository.create(validated_data)
            return AppointmentSchemaDTO().dump(new_appointment), 201
        except Exception:
            return {"error": "Erro ao cadastrar agendamento."}, 500

    def update(id, validated_data):
        """Atualiza um agendamento."""
        appointment_db = AppointmentRepository.get_by_id(id)
        if not appointment_db:
            return {"error": "Agendamento não encontrado"}, 404
        
        pet = PetRepository.get_by_id(validated_data["pet_id"])
        if not pet:
            return {"error": "Pet informado não existe."}, 404

        try:
            updated_appointment = AppointmentRepository.update(appointment_db, validated_data)
            return AppointmentSchemaDTO().dump(updated_appointment), 200
        except Exception:
            return {"error": "Erro ao atualizar agendamento."}, 500

    def delete(id):
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
