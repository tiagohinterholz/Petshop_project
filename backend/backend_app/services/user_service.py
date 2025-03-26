from backend_app.repository.user_repository import UserRepository
from backend_app.schema_dto.user_schema_dto import UserSchemaDTO
from backend_app.schema_dto.user_update_schema_dto import UserUpdateSchemaDTO
from sqlalchemy.exc import IntegrityError
from backend_app.models.user_model import ProfileEnum

class UserService:
    def list_users():
        """Lista todos os pets cadastrados."""
        users = UserRepository.list_all()
        return UserSchemaDTO(many=True).dump(users), 200

    def list_user_id(id):
        """Busca usuário pelo ID."""
        user = UserRepository.get_user_by_id(id)
        if not user:
            return {"error": "Usuário não encontrado"}, 404
        return UserSchemaDTO().dump(user), 200 

    def register(validated_data):
        """Cadastra um novo usuário."""
        try:
            # Valida se o usuário está tentando criar um ADMIN
            if validated_data["profile"] == ProfileEnum.ADMIN:
                return {"error": "Não é permitido criar um usuário ADMIN via Rota API"}, 403
            new_user, status = UserRepository.create(validated_data)
            
            return UserSchemaDTO().dump(new_user), status
        except IntegrityError:
            return {"error": "Problema nos dados de cadastro"}, 422  # Melhor mensagem de erro
        except Exception:
            return {"error": "Erro inesperado ao cadastrar Usuário"}, 500

    def update(cpf, validated_data):
        """Atualiza um usuário."""
        user_db = UserRepository.get_user_by_id(id)
        
        try:
            # Valida se o usuário está tentando atualizar seu perfil para um ADMIN
            if validated_data.get("profile") == ProfileEnum.ADMIN:
                return {"error": "Não é permitido atualizar um usuário para ADMIN via Rota API"}, 403
            
            updated_user = UserRepository.update(user_db, validated_data)
            return UserUpdateSchemaDTO().dump(updated_user), 200
        except Exception:
            return {"error": "Erro ao atualizar Usuário."}, 500

    def delete(id):
        """Exclui um usuário pelo ID."""
        user = UserRepository.get_user_by_id(id)
        if not user:
            return {"error": "Usuário não encontrado"}, 404  

        try:
            success = UserRepository.delete(user)
            if success:
                return {"message": "Usuário deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir Usuário."}, 500

