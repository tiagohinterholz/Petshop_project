from backend_app.repository.address_repository import AddressRepository
from backend_app.repository.client_repository import ClientRepository
class AddressService:

    @staticmethod
    def list_addresses():
        """Lista todos os endereços cadastrados."""
        return AddressRepository.list_all(), 200
    
    @staticmethod
    def list_address_id(id):
        """Retorna um endereço pelo ID."""
        address = AddressRepository.get_by_id(id)
        if not address:
            return {"error": "Endereço não encontrado"}, 404
        return address, 200
    
    @staticmethod
    def register_address(validated_data):
        """Cadastra um novo endereço para um cliente."""
        client = ClientRepository.get_by_id(validated_data["client_id"])
        if not client:
            return {"error": "Cliente informado não existe."}, 400
               
        try:
            new_address = AddressRepository.create(validated_data)
            return new_address, 201
        except Exception:
            return {"error": "Erro ao cadastrar endereço."}, 500
        
    @staticmethod
    def update_address(id, validated_data):
        """Atualiza um endereço."""
        address_db = AddressRepository.get_by_id(id)
        if not address_db:
            return {"error": "Endereço não encontrado"}, 404
        
        client = ClientRepository.get_by_id(validated_data["client_id"])
        if not client:
            return {"error": "O cliente informado não existe."}, 400

        try:
            updated_address = AddressRepository.update(address_db, validated_data)
            return updated_address, 200
        except Exception:
            return {"error": "Erro ao atualizar endereço."}, 500
        
    @staticmethod
    def delete_address(id):
        """Exclui um endereço."""
        address = AddressRepository.get_by_id(id)
        if not address:
            return {"error": "Endereço não encontrado"}, 404
            
        try:
            success = AddressRepository.delete(address)
            if success:
                return {"message": "Endereço deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir endereço."}, 500
    
