from backend_app import db
from backend_app.models.breed_model import Breed

class BreedRepository:
    """Classe responsável pelo acesso ao banco de dados para raças."""

    @staticmethod
    def get_by_description(description):
        """Busca uma raça pelo campo description."""
        return db.session.query(Breed).filter_by(description=description).first()
    
    @staticmethod
    def list_all():
        """Lista todos raças."""
        return Breed.query.all()

    @staticmethod
    def get_by_id(id):
        """Busca uma raça pelo ID."""
        return db.session.get(Breed, id)

    @staticmethod
    def create(validated_data):
        """Cria uma nova raça."""
        new_breed = Breed(
            description=validated_data["description"]
            )
        db.session.add(new_breed)
        db.session.commit()
        return new_breed   
    
    @staticmethod
    def update(breed, new_data):
        """Atualiza uma raça no banco de dados."""
        breed.description = new_data["description"]
        """Confirma as alterações no banco de dados."""
        db.session.commit()
        return breed

    @staticmethod
    def delete(breed):
        """Exclui uma raça."""
        db.session.delete(breed)
        db.session.commit()
        return True