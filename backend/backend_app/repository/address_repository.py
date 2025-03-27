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
    def get_by_client_id(client_id):
        """Busca um endereço pelo CLIENT ID."""
        return db.session.query(Address).filter_by(client_id=client_id).first()

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
        db.session.refresh(new_address)
        return new_address

    @staticmethod
    def update(address, new_data):
        """Atualiza um endereço no banco de dados."""
        address.client_id = new_data.get("client_id", address.client_id)
        address.street = new_data.get("street", address.street)
        address.city = new_data.get("city", address.city)
        address.neighborhood = new_data.get("neighborhood", address.neighborhood)
        address.complement = new_data.get("complement", address.complement)
        """Confirma as alterações no banco de dados."""
        db.session.commit()
        return address

    @staticmethod
    def delete(address):
        """Exclui um endereço."""
        db.session.delete(address)
        db.session.commit()
        return True