from backend_app.repository.procedure_repository import ProcedureRepository
from backend_app.schema_dto.procedure_schema_dto import ProcedureSchemaDTO
from backend_app.schema_dto.procedure_update_schema_dto import ProcedureUpdateSchemaDTO

class ProcedureService:

    def list_procedures():
        """Lista todos os procedimentos cadastrados."""
        procedures = ProcedureRepository.list_all()
        return ProcedureSchemaDTO(many=True).dump(procedures), 200
    
    def list_procedure_id(id):
        """Retorna um procedimento pelo ID."""
        procedure = ProcedureRepository.get_by_id(id)
        if not procedure:
            return {"error": "Endereço não encontrado"}, 404
        return ProcedureSchemaDTO().dump(procedure), 200   
    
    def register(validated_data):
        """Cadastra um novo procedimento"""               
        try:
            new_procedure = ProcedureRepository.create(validated_data)
            return ProcedureSchemaDTO().dump(new_procedure), 201
        except Exception:
            return {"error": "Erro ao cadastrar procedimento."}, 500
        
    def update(id, validated_data):
        """Atualiza um procedimento."""
        procedure_db = ProcedureRepository.get_by_id(id)

        try:
            updated_procedure = ProcedureRepository.update(procedure_db, validated_data)
            return ProcedureUpdateSchemaDTO().dump(updated_procedure), 200
        except Exception:
            return {"error": "Erro ao atualizar procedimento."}, 500
        
    def delete(id):
        """Exclui um procedimento."""
        procedure = ProcedureRepository.get_by_id(id)
        if not procedure:
            return {"error": "Poocedimento não encontrado"}, 404
            
        try:
            success = ProcedureRepository.delete(procedure)
            if success:
                return {"message": "Procedimento deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir procedimento."}, 500
    
