from backend_app import db
from backend_app.models.pet_model import Pet
from backend_app.repository.pet_repository import PetRepository
from backend_app.repository.breed_repository import BreedRepository
from backend_app.repository.client_repository import ClientRepository

class PetService:
    
    def list_pets():
        """Lista todos os pets cadastrados."""
        return PetRepository.list_all(), 200

        
    def list_pet_id(id):
        """Busca um pet pelo ID."""
        pet = PetRepository.get_by_id(id)
        if not pet:
            return {"error": "Pet não encontrado"}, 404
        return pet, 200
        
    def register(validated_data):
        """Cadastra um novo pet."""
        existing_client = ClientRepository.get_by_id(validated_data["client_id"])
        if not existing_client: # verifica se existe um cliente
            return {"error":"Cliente informado não cadastrado."}, 400
        
        existing_breed = PetRepository.get_by_id(validated_data["breed_id"])
        if not existing_breed: # verifica se ja existe uma raça cadastrada
            return {"error":"Raça informada não cadastrada."}, 400 
        
        try:
            new_pet = PetRepository.create(validated_data)
            return new_pet, 201 
        except Exception:
            return {"error": "Erro ao cadastrar Pet"}, 500
    
        
    def update(id, validated_data):
        """Atualiza os dados de um pet."""
        pet_db = PetRepository.get_by_id(id)
        if not pet_db:
            return {"error": "Pet não encontrado"}, 404
        
        existing_client = ClientRepository.get_by_id(validated_data["client_id"])
        if not existing_client: # verifica se existe um cliente
            return {"error":"Cliente informado não cadastrado."}, 400
        
        existing_breed = PetRepository.get_by_id(validated_data["breed_id"])
        if not existing_breed: # verifica se ja existe uma raça cadastrada
            return {"error":"Raça informada não cadastrada."}, 400 
               
        try:
            updated_pet = PetRepository.update(pet_db, validated_data)
            return updated_pet, 200
        except Exception:
            return {"error": "Erro ao atualizar pet."}, 500
        
    def delete(id):
        """Exclui um pet pelo ID."""
        pet = PetRepository.get_by_id(id)
        if not pet:
            return {"error": "Pet não encontrado"}, 404  

        try:
            success = PetRepository.delete(pet)
            if success:
                return {"message": "Pet deletado com sucesso"}, 200
        except Exception:
            return {"error": "Erro ao excluir Pet."}, 500
    
    
