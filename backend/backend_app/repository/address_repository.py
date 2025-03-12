from backend_app import db
from backend_app.models.address_model import Address

class AddressRepository:   
    @staticmethod
    def list_all():
        """Lista todos os endereços."""
        return Address.query.all()

    @staticmethod
    def get_by_id(id):
        """Busca um endereço pelo ID."""
        return db.session.get(Address, id)

    @staticmethod
    def create(validated_data):
        """Cria um novo endereço."""
        new_address = Address(
            client_id=validated_data["client_id"],
            street=validated_data["street"],
            city=validated_data["city"],
            neighborhood=validated_data["neighborhood"],
            complement=validated_data["complement"]
            )
        db.session.add(new_address)
        db.session.commit()
        return new_address

    @staticmethod
    def update(address, new_data):
        """Atualiza um endereço no banco de dados."""
        address.client_id = new_data["client_id"]
        address.street = new_data["street"]
        address.city = new_data["city"]
        address.neighborhood = new_data["neighborhood"]
        address.complement = new_data["complement"]
        """Confirma as alterações no banco de dados."""
        db.session.commit()
        return address

    @staticmethod
    def delete(address):
        """Exclui um endereço."""
        db.session.delete(address)
        db.session.commit()
        return True