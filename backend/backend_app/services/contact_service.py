from backend_app.repository.contact_repository import ContactRepository
from backend_app.repository.client_repository import ClientRepository
from backend_app.schema_dto.contact_schema_dto import ContactSchemaDTO
class ContactService:

    @staticmethod
    def list_contacts():
        """Lista todos os contatos."""
        contacts = ContactRepository.list_all()
        return ContactSchemaDTO(many=True).dump(contacts), 200
    
    def list_contact_id(id):
        """Busca um contato pelo ID."""
        contact = ContactRepository.get_by_id(id)
        if not contact:
            return {"error": "Contato não encontrado"}, 404
        return ContactSchemaDTO().dump(contact), 200
            
    def register(validated_data):
        """Cadastra um novo contato."""
        existing_client = ClientRepository.get_by_id(validated_data["client_id"])
        if not existing_client: # verifica se ja existe CPF cadastrado
            return {"error":"Cliente informado não cadastrado."}, 400        
        try: 
            new_contact = ContactRepository.create(validated_data)
            return ContactSchemaDTO().dump(new_contact), 201
        except Exception:
            return {"error": "Erro ao cadastrar contato."}, 500
            
    def update(id, validated_data):
        """Atualiza um contato."""
        contact_db = ContactRepository.get_by_id(id)
        if not contact_db:
            return {"error": "Contato não encontrado"}, 404
        
        existing_client = ClientRepository.get_by_id(validated_data["id"])
        if not existing_client: # verifica se ja existe CPF cadastrado
            return {"error":"Cliente informado não cadastrado."}, 400
        try:
            updated_contact = ContactRepository.update(contact_db, validated_data)
            return ContactSchemaDTO().dump(updated_contact), 200
        except Exception:
            return {"error": "Erro ao atualizar contato."}, 500

    def delete(id):
        """Exclui um contato."""
        contact = ContactRepository.get_by_id(id)
        if not contact:
            return {"error": "Contato não encontrado"}, 404  
        try:
            success = ContactRepository.delete(contact)
            if success:
                return {"message": "Contato deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir contato."}, 500
