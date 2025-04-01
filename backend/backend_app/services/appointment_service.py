from backend_app.repository.appointment_repository import AppointmentRepository
from backend_app.repository.procedure_repository import ProcedureRepository
from backend_app.repository.pet_repository import PetRepository
from backend_app.schema_dto.appointment_schema_dto import AppointmentSchemaDTO
from datetime import timedelta
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
        """Retorna um agendamento pelo pet ID."""
        appointments = AppointmentRepository.get_by_pet_id(pet_id)
        if not appointments:
            return [], 200
        return AppointmentSchemaDTO(many=True).dump(appointments), 200

    def register(validated_data):
        """Cadastra um novo agendamento."""
        
        pet = PetRepository.get_by_id(validated_data["pet_id"])
        if not pet:
            return {"error": "Pet informado não existe."}, 404
        
        procedure_id = validated_data["procedure_id"]
        new_start = validated_data["date_appoint"]
        procedure = ProcedureRepository.get_by_id(procedure_id)
        new_duration = procedure.time_service
        new_end = new_start + timedelta(minutes=new_duration)
        
        if not (8 <= new_start.hour < 17 or (new_start.hour == 17 and new_start.minute == 0)):
            return {"error": "Agendamentos permitidos apenas após 08:00"}, 400

        if new_end.hour > 17 or (new_end.hour == 17 and new_end.minute > 0):
            return {"error": "Horário ultrapassa o expediente permitido - 17:00h"}, 400
        
        start_of_day = new_start.replace(hour=8, minute=0, second=0, microsecond=0)
        end_of_day = new_start.replace(hour=18, minute=00, second=00, microsecond=0)

        existing_appointments = AppointmentRepository.list_all_interval_time(start_of_day, end_of_day)

        for appt in existing_appointments:
            appt_start = appt.date_appoint
            appt_end = appt_start + timedelta(minutes=appt.procedure.time_service)

            # Se houver interseção, já era
            if (new_start < appt_end and new_end > appt_start):
                return {"error": "Horário indisponível. Já existe agendamento nesse intervalo."}, 400
        
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
        
        new_start = validated_data.get("date_appoint", appointment_db.date_appoint)
        procedure_id = validated_data.get("procedure_id", appointment_db.procedure_id)
        procedure = ProcedureRepository.get_by_id(procedure_id)
        if not procedure:
            return {"error": "Procedimento informado não existe."}, 404
        new_duration = procedure.time_service
        new_end = new_start + timedelta(minutes=new_duration)
        
        if not (8 <= new_start.hour < 17 or (new_start.hour == 17 and new_start.minute == 0)):
            return {"error": "Agendamentos permitidos apenas após 08:00"}, 400

        if new_end.hour > 17 or (new_end.hour == 17 and new_end.minute > 0):
            return {"error": "Horário ultrapassa o expediente permitido - 17:00h"}, 400
        
        start_of_day = new_start.replace(hour=8, minute=0, second=0, microsecond=0)
        end_of_day = new_start.replace(hour=18, minute=00, second=00, microsecond=0)

        existing_appointments = AppointmentRepository.list_all_interval_time(start_of_day, end_of_day)

        for appt in existing_appointments:
            appt_start = appt.date_appoint
            appt_end = appt_start + timedelta(minutes=appt.procedure.time_service)

            # Se houver interseção, já era
            if (new_start < appt_end and new_end > appt_start):
                return {"error": "Horário indisponível. Já existe agendamento nesse intervalo."}, 400
    
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
