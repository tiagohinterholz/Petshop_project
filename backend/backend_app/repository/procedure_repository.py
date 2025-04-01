from backend_app import db
from backend_app.models.procedure_model import Procedure

class ProcedureRepository:
    
    @staticmethod
    def list_all():
        """Lista todos os procedimentos."""
        return Procedure.query.all()

    @staticmethod
    def get_by_id(id):
        """Busca um procedimento pelo ID."""
        return db.session.get(Procedure, id)

    @staticmethod
    def create(validated_data):
        """Cria um novo procedimento."""
        new_procedure = Procedure(
            price=validated_data["price"],
            description=validated_data["description"],
            time_service=validated_data["time_service"]
            )
        db.session.add(new_procedure)
        db.session.commit()
        db.session.refresh(new_procedure)
        return new_procedure

    @staticmethod
    def update(procedure, new_data):
        """Atualiza um agendamento no banco de dados."""
        procedure.price = new_data.get("price", procedure.price)
        procedure.description = new_data.get("description", procedure.description)
        procedure.time_service = new_data.get("time_service", procedure.time_service)
        """Confirma as alterações no banco de dados."""
        db.session.commit()
        return procedure

    @staticmethod
    def delete(procedure):
        """Exclui um procedimento."""
        db.session.delete(procedure)
        db.session.commit()
        return True