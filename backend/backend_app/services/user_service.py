from backend_app.repository.user_repository import UserRepository

class UserService:
    def list_users():
        """Lista todos os pets cadastrados."""
        return UserRepository.list_all(), 200

    def list_user_id(cpf):
        """Busca usuário pelo CPF."""
        user = UserRepository.get_user_by_cpf(cpf)
        if not user:
            return {"error": "User não encontrado"}, 404
        return user, 200 

    def register(validated_data):
        """Cadastra um novo usuário."""
        try:
            new_user = UserRepository.create(validated_data)
            return new_user, 201 
        except Exception:
            return {"error": "Erro ao cadastrar Pet"}, 500

    def update(cpf, validated_data):
        """Atualiza um usuário."""
        user_db = UserRepository.get_user_by_cpf(cpf)
        if not user_db:
            return {"error": "Usuário não encontrado"}, 404  
        
        try:
            updated_user = UserRepository.update(user_db, validated_data)
            return updated_user, 200
        except Exception:
            return {"error": "Erro ao atualizar User."}

    def delete(cpf):
        """Exclui um usuário pelo CPF."""
        user = UserRepository.get_user_by_cpf(cpf)
        if not user:
            return {"error": "User não encontrado"}, 404  

        try:
            success = UserRepository.delete(user)
            if success:
                return {"message": "User deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir user."}, 500
