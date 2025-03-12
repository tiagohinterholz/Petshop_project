from backend_app import db
from backend_app.models.pet_model import Pet
from backend.backend_app.repository.pet_repository import PetSchema 
from marshmallow import ValidationError

def list_pets():
    """Lista todos os pets cadastrados."""
    try:
        pets = Pet.query.all()
        return PetSchema(many=True).dump(pets), 200
    except Exception as e:
        return {"error": f"Erro ao listar todos os pets: {str(e)}"}, 500
    
def register_pet(pet_data):
    """Cadastra um novo pet."""
    schema = PetSchema()
    
    try:
        validated_data = schema.load(pet_data)
    except ValidationError as err:
        return {"error": err.messages}, 400  
    
    pet_db = Pet(
        client_id=validated_data.client_id,
        breed_id=validated_data.breed_id,
        birth_date=validated_data.birth_date,
        name=validated_data.name
    )

    try:
        db.session.add(pet_db)
        db.session.commit()
        return schema.dump(pet_db), 201 
    except Exception as e:
        db.session.rollback()  # Evita inconsistências no banco
        return {"error": f"Erro ao cadastrar pet: {str(e)}"}, 500
    
def list_pet_id(id):
    """Busca um pet pelo ID."""
    try:
        pet = db.session.get(Pet, id)
        if not pet:
            return {"error": "Pet não encontrado"}, 404
        return PetSchema().dump(pet), 200 
    except Exception as e:
        return {"error": f"Erro ao buscar pet: {str(e)}"}, 500
    
def update_pet(pet_db, new_pet_data):
    """Atualiza os dados de um pet."""
    if not pet_db:
        return {"error": "Pet não encontrado"}, 404
    
    try:
        pet_db.client_id = new_pet_data["client_id"]
        pet_db.breed_id = new_pet_data["breed_id"] 
        pet_db.birth_date = new_pet_data["birth_date"]
        pet_db.name = new_pet_data["name"]
        
        db.session.commit()
        return PetSchema().dump(pet_db), 200
    except Exception as e:
        return {"error": f"Erro ao atualizar dados do pet: {e}"}, 500
    
def delete_pet(id):
    """Exclui um pet pelo ID."""
    try:
        pet = db.session.get(Pet, id)
        if not pet:
            return {"error": "Pet não encontrado"}, 404
        db.session.delete(pet)
        db.session.commit()
        return {"message": "Pet deletado com sucesso"}, 200 
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao excluir pet: {str(e)}"}, 500
    
    
