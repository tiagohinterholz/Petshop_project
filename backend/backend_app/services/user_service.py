from backend_app.repository.user_repository import UserRepository
from backend_app.schema_dto.user_schema_dto import UserSchemaDTO
from sqlalchemy.exc import IntegrityError
import logging

class UserService:
    def list_users():
        """Lista todos os pets cadastrados."""
        users = UserRepository.list_all()
        return UserSchemaDTO(many=True).dump(users), 200

    def list_user_id(cpf):
        """Busca usuário pelo CPF."""
        user = UserRepository.get_user_by_cpf(cpf)
        if not user:
            return {"error": "Usuário não encontrado"}, 404
        return UserSchemaDTO().dump(user), 200 

    def register(validated_data):
        """Cadastra um novo usuário."""
        try:
            new_user, status = UserRepository.create(validated_data)
            return UserSchemaDTO().dump(new_user), status
        except IntegrityError:
            return {"error": "Problema nos dados de cadastro"}, 400  # Melhor mensagem de erro
        except Exception:
            return {"error": "Erro inesperado ao cadastrar Usuário"}, 500

    def update(cpf, validated_data):
        """Atualiza um usuário."""
        user_db = UserRepository.get_user_by_cpf(cpf)
        if not user_db:
            return {"error": "Usuário não encontrado"}, 404  
        
        try:
            updated_user = UserRepository.update(user_db, validated_data)
            return UserSchemaDTO().dump(updated_user), 200
        except Exception:
            return {"error": "Erro ao atualizar Usuário."}, 500

    def delete(cpf):
        """Exclui um usuário pelo CPF."""
        user = UserRepository.get_user_by_cpf(cpf)
        if not user:
            return {"error": "Usuário não encontrado"}, 404  

        try:
            success = UserRepository.delete(user)
            if success:
                return {"message": "Usuário deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir Usuário."}, 500

