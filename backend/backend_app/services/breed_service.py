from backend_app import db
from backend_app.models.breed_model import Breed
from backend_app.schemas.breed_schema import BreedSchema
from marshmallow import ValidationError

def list_breeds():
    """Lista todas as raças."""
    try:
        breeds = Breed.query.all()
        return BreedSchema(many=True).dump(breeds), 200
    except Exception as e:
        return {"error": f"Erro ao listar raças: {str(e)}"}, 500
    
def register_breed(breed_data):
    """Cadastra uma nova raça."""
    
    schema = BreedSchema()
    
    try:
        validated_data = schema.load(breed_data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    
    try:         
        breed_db = Breed(description=validated_data.description)
        db.session.add(breed_db)
        db.session.commit()
        return schema.dump(breed_db), 201
    except Exception as e:
        db.session.rollback()  # Evita inconsistências no banco
        return {"error": f"Erro ao cadastrar raça: {str(e)}"}, 500

def list_breed_id(id):
    """Busca uma raça pelo ID."""
    try:
        breed = db.session.query.get(Breed, id)
        if not breed:
            return {"error": "Raça não encontrada"}, 404 
        return BreedSchema().dump(breed), 200  
    except Exception as e:
        return {"error": f"Erro ao buscar raça: {str(e)}"}, 500
    
def update_breed(breed_db, new_breed_data):
    """Atualiza uma raça."""
    if not breed_db:
        return {"error": "Raça não encontrada"}, 404  

    try:
        breed_db.description = new_breed_data["description"]
        db.session.commit()  
        return BreedSchema().dump(breed_db), 200 
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao atualizar raça: {str(e)}"}, 500

def delete_breed(id):
    """Exclui uma raça."""
    try:
        breed = db.session.get(Breed, id)
        if not breed:
            return {"error": "Raça não encontrada"}, 404
        
        db.session.delete(breed)
        db.session.commit()
        return {"message": "Raça deletado com sucesso"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao excluir raça: {str(e)}"}, 500

