from backend_app import db 
from backend_app.models.pet_model import Pet

class PetRepository:
    @staticmethod
    def list_all():
        """Lista todos pets."""
        return Pet.query.all()
    
    @staticmethod
    def get_by_id(id):
        """Busca um contato pelo ID."""
        return db.session.get(Pet, id)
    
    @staticmethod
    def create(validated_data):
        """Cria um novo pet."""
        new_pet = Pet(
        client_id=validated_data["client_id"],
        breed_id=validated_data["breed_id"],
        birth_date=validated_data["birth_date"],
        name=validated_data["name"]
        )
        db.session.add(new_pet)
        db.session.commit()
        db.session.refresh(new_pet)
        return new_pet
    
    @staticmethod
    def update(pet, new_data):
        """Atualiza um pet no banco de dados."""
        pet.client_id = new_data["client_id"]
        pet.breed_id = new_data["breed_id"] 
        pet.birth_date = new_data["birth_date"]
        pet.name = new_data["name"]
        """Confirma as alterações no banco de dados."""
        db.session.commit()
        return pet

    @staticmethod
    def delete(pet):
        """Exclui um pet."""
        db.session.delete(pet)
        db.session.commit()
        return True