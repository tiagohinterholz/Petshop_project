from backend_app import db
from backend_app.models.pet_model import Pet
from backend_app.models.breed_model import Breed
from backend_app.models.client_model import Client
from backend_app.schemas.pet_schema import PetSchema  

def register_pet(pet_data):
    """Cadastra um novo pet."""
    
    client_exists = db.session.get(Client, pet_data["client_id"])  
    breed_exists = db.session.get(Breed, pet_data["breed_id"])
    
    if not client_exists:
        return {"error": "Cliente não encontrado"}, 404 
    
    if not breed_exists:
        return {"error": "Raça não encontrada"}, 404 
    
    pet_db = Pet(
        client_id=pet_data["client_id"],
        breed_id=pet_data["breed_id"],
        birth_date=pet_data["birth_date"],
        name=pet_data["name"]
    )

    db.session.add(pet_db)
    db.session.commit()

    return PetSchema().dump(pet_db), 201 

def list_pets():
    """Lista todos os pets cadastrados."""
    pets = Pet.query.all()
    return PetSchema(many=True).dump(pets), 200

def list_pet_id(id):
    """Busca um pet pelo ID."""
    pet = db.session.get(Pet, id)
    if not pet:
        return {"error": "Pet não encontrado"}, 404
    return PetSchema().dump(pet), 200 

def update_pet(pet_db, new_pet_data):
    """Atualiza os dados de um pet."""
    if not pet_db:
        return {"error": "Pet não encontrado"}, 404
    
    pet_db.client_id = new_pet_data["client_id"]
    pet_db.breed_id = new_pet_data["breed_id"] 
    pet_db.birth_date = new_pet_data["birth_date"]
    pet_db.name = new_pet_data["name"]
    
    db.session.commit()
    
    return PetSchema().dump(pet_db), 200
def delete_pet(pet_db):
    """Exclui um pet pelo ID."""
    if not pet_db:
        return {"error": "Pet não encontrado"}, 404 
    
    db.session.delete(pet_db)
    db.session.commit()
    
    return {"message": "Pet deletado com sucesso"}, 204 
