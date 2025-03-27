from backend_app import db
from backend_app.models.client_model import Client
from datetime import datetime, timezone

class ClientRepository:
    
    @staticmethod
    def list_all():
        """Lista todos clientes."""
        return Client.query.all()

    @staticmethod
    def get_by_id(id):
        """Busca um cliente pelo ID."""
        return db.session.get(Client, id)

    @staticmethod
    def create(validated_data):
        """Cria um novo cliente."""
        new_client = Client(
            name=validated_data["name"],
            user_id=validated_data["user_id"],
            register_date = datetime.now(timezone.utc).date()
            )
        db.session.add(new_client)
        db.session.commit()
        db.session.refresh(new_client)
        
        return new_client
    
    # @staticmethod
    # def update(client, new_data):
    #     """Atualiza um cliente no banco de dados."""
    #     client.name = new_data["name"]
    #     client.register_date = datetime.now(timezone.utc).date()
    #     """Confirma as alterações no banco de dados."""
    #     db.session.commit()
    #     return client

    @staticmethod
    def delete(client):
        """Exclui um cliente."""
        db.session.delete(client)
        db.session.commit()
        return True
