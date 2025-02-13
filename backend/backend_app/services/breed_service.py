from backend_app import db
from backend_app.models.breed_model import Breed

def register_breed(breed):
    breed_db = Breed(description=breed.description)
    db.session.add(breed_db)
    db.session.commit()
    return breed_db

def list_breeds():
    return Breed.query.all()
    
def list_breed_id(id):
    breed = Breed.query.filter_by(id=id).first()
    if not breed:
        return None
    return breed

def update_breed(breed_db, new_breed):
    if not breed_db:
        return None 
    breed_db.description = new_breed.description
    db.session.commit()
    return breed_db

def delete_breed(breed):
    if not breed:
        return None
    db.session.delete(breed)
    db.session.commit()
    return True


