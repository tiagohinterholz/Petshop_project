from backend.backend_app.repository.breed_repository import BreedRepository

class BreedService:

    @staticmethod
    def list_breeds():
        """Lista todas as raças."""
        return BreedRepository.list_all(), 200
    
    @staticmethod
    def list_breed_by_id(id):
        """Busca uma raça pelo ID."""
        
        breed = BreedRepository.get_by_id(id)
        if not breed:
            return {"error": "Raça não encontrada"}, 404
        return breed, 200
    
    @staticmethod
    def register_breed(validated_data):
        """Cadastra uma nova raça."""
       
        existing_breed = BreedRepository.get_by_description(validated_data["description"])
        if existing_breed:
            return {"error": "Já existe uma raça cadastrada com essa descrição."}, 400
        
        try:         
            new_breed = BreedRepository.create(validated_data)
            return new_breed, 201
        except Exception:
            return {"error": f"Erro ao cadastrar raça."}, 500
    
    @staticmethod
    def update_breed(id, validated_data):
        """Atualiza uma raça."""
        breed_db = BreedRepository.get_by_id(id)
        if not breed_db:
            return {"error": "Raça não encontrada"}, 404  

        try:
            updated_breed = BreedRepository.update(breed_db, validated_data)
            return updated_breed, 200
        except Exception:
            return {"error": f"Erro ao atualizar raça."}, 500

    @staticmethod
    def delete_breed(id):
        """Exclui uma raça."""
        
        breed = BreedRepository.get_by_id(id)
        if not breed:
            return {"error": "Raça não encontrada"}, 404
        
        try:
            success = BreedRepository.delete(breed)
            if success:
                return {"message": "Raça deletada com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir raça."}, 500

