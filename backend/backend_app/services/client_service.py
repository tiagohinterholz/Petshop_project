from backend_app.repository.client_repository import ClientRepository
from backend_app.repository.user_repository import UserRepository

class ClientService:
    
    @staticmethod
    def list_clients():
        """Listar todos os clientes."""
        return ClientRepository.list_all(), 200  
    
    @staticmethod
    def list_client_id(id):
        """Buscar um cliente pelo ID."""
        
        client = ClientRepository.get_by_id(id)
        if not client:
            return {"error": "Cliente não encontrado"}, 404
        return client, 200
    
    @staticmethod
    def register_client(validated_data):
        """Cadastrar um novo cliente."""
     
        existing_client = ClientRepository.get_client_by_cpf(validated_data["cpf"])
        if existing_client: # verifica se ja existe CPF cadastrado
            return {"error":"CPF já cadastrado para outro cliente."}, 400
           
        existing_user = UserRepository.get_user_by_cpf(validated_data["cpf"])
        if not existing_user: # verifica se não existe cpf em USER pq dai nao da pra cadastrar client
            return {"error": "Não existe um usuário cadastrado com esse CPF."}, 400
                
        try:
            new_client = ClientRepository.create(validated_data)
            return new_client, 201 
        except Exception:
            return {"error": "Erro ao cadastrar cliente."}, 500
            
    def update_client(id, validated_data):
        """Atualizar um cliente."""
        client_db = ClientRepository.get_by_id(id)
        if not client_db:
            return {"error": "Cliente não encontrado"}, 404  
        # na atualização verificar de novo pq se passa um cpf que já existe nao pode atualizar
        existing_client = ClientRepository.get_client_by_cpf(validated_data["cpf"])
        if existing_client: # verifica se ja existe CPF cadastrado
            return {"error":"CPF já cadastrado para outro cliente."}, 400
        # na atualização verificar de novo pq se passa um cpf que nao tem user, nao pode atualizar
        existing_user = UserRepository.get_user_by_cpf(validated_data["cpf"])
        if not existing_user: # verifica se não existe cpf em USER pq dai nao da pra cadastrar client
            return {"error": "Não existe um usuário cadastrado com esse CPF."}, 400
        
        try:
            updated_client = ClientRepository.update(client_db, validated_data)
            return updated_client, 200
        except Exception:
            return {"error": "Erro ao atualizar cliente."}, 500
            
    def delete_client(id):
        """Excluir um cliente."""
        client = ClientRepository.get_by_id(id)
        if not client:
            return {"error": "Cliente não encontrado"}, 404
        
        try:
            success = ClientRepository.delete(client)
            if success:
                return {"message": "Cliente deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir cliente."}, 500