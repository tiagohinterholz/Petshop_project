from backend_app import db
from backend_app.repository.pet_repository import PetRepository
from backend_app.repository.breed_repository import BreedRepository
from backend_app.repository.client_repository import ClientRepository
from backend_app.schema_dto.pet_schema_dto import PetSchemaDTO
class PetService:
    
    def list_pets():
        """Lista todos os pets cadastrados."""
        pets = PetRepository.list_all()
        return PetSchemaDTO(many=True).dump(pets), 200     
        
    def list_pet_id(id):
        """Busca um pet pelo ID."""
        pet = PetRepository.get_by_id(id)
        if not pet:
            return {"error": "Pet não encontrado"}, 404
        return PetSchemaDTO().dump(pet), 200
        
    def list_pet_client_id(client_id):
        """Retorna um pet pelo client ID."""
        pets = PetRepository.get_by_client_id(client_id)
        if not pets:
            return [], 200
        return PetSchemaDTO(many=True).dump(pets), 200
    
    def register(validated_data):
        """Cadastra um novo pet."""
        existing_client = ClientRepository.get_by_id(validated_data["client_id"])
        if not existing_client: # verifica se existe um cliente
            return {"error":"Cliente informado não cadastrado."}, 404
        
        existing_breed = BreedRepository.get_by_id(validated_data["breed_id"])
        if not existing_breed: # verifica se ja existe uma raça cadastrada
            return {"error":"Raça informada não cadastrada."}, 404 
        
        try:
            new_pet = PetRepository.create(validated_data)
            return PetSchemaDTO().dump(new_pet), 201 
        except Exception:
            return {"error": "Erro ao cadastrar Pet"}, 500
    
        
    def update(id, validated_data):
        """Atualiza os dados de um pet."""
        pet_db = PetRepository.get_by_id(id)
        client_id = validated_data.get("client_id")
        breed_id = validated_data.get("breed_id")
        
        if client_id:       
            client = ClientRepository.get_by_id(client_id)
            if not client:
                return {"error": "Cliente informado não existe."}, 404
        if breed_id:       
            breed = BreedRepository.get_by_id(breed_id)
            if not breed:
                return {"error": "Raça informado não existe."}, 404
               
        try:
            updated_pet = PetRepository.update(pet_db, validated_data)
            return PetSchemaDTO().dump(updated_pet), 200
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
    
    
