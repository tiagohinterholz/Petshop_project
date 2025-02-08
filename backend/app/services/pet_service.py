from app import db
from app.models.pet_model import Pet
from app.models.breed_model import Breed
from app.models.client_model import Client

def register_pet(pet):
    
    client_exists = Client.query.get(pet.client_id)
    breed_exists = Breed.query.get(pet.breed_id)
    
    if not client_exists:
        return None
    
    if not breed_exists:
        return None
    
    pet_db = Pet(
        client_id = pet.client_id,
        breed_id = pet.breed_id,
        birth_date = pet.birth_date,
        name = pet.name
        )

    db.session.add(pet_db)
    db.session.commit()
    return pet_db

def list_pets():
    return Pet.query.all()

def list_pet_id(id):
    return Pet.query.filter_by(id=id).first()

def update_pet(pet_db, new_pet):
    if not pet_db:
        return None
    pet_db.client_id = new_pet.client_id
    pet_db.birth_date = new_pet.birth_date
    pet_db.name = new_pet.name
    db.session.commit()
    return pet_db

def delete_pet(pet):
    if not pet:
        return False
    db.session.delete(pet)
    db.session.commit()
    return True