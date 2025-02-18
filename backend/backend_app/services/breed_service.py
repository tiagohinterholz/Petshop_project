from backend_app import db
from backend_app.models.breed_model import Breed
from backend_app.schemas.breed_schema import BreedSchema

def register_breed(breed_data):
    """Cadastra uma nova raça."""
    breed_db = Breed(description=breed_data["description"])
    db.session.add(breed_db)
    db.session.commit()
    
    return BreedSchema().dump(breed_db), 201 

def list_breeds():
    """Lista todas as raças."""
    breeds = Breed.query.all()
    return BreedSchema(many=True).dump(breeds), 200

def list_breed_id(id):
    """Busca uma raça pelo ID."""
    breed = Breed.query.get(id)
    if not breed:
        return {"error": "Raça não encontrada"}, 404 
    return BreedSchema().dump(breed), 200  

def update_breed(breed_db, new_breed_data):
    """Atualiza uma raça."""
    if not breed_db:
        return {"error": "Raça não encontrada"}, 404  

    breed_db.description = new_breed_data["description"]
    db.session.commit()
    
    return BreedSchema().dump(breed_db), 200 

def delete_breed(breed):
    """Exclui uma raça."""
    if not breed:
        return {"error": "Raça não encontrada"}, 404  

    db.session.delete(breed)
    db.session.commit()
    
    return {}, 204
