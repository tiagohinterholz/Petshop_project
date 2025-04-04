from backend_app import db
from backend_app.models.contact_model import Contact

class ContactRepository:
    @staticmethod
    def list_all():
        """Lista todos contatos."""
        return Contact.query.all()

    @staticmethod
    def get_by_id(id):
        """Busca um contato pelo ID."""
        return db.session.get(Contact, id)
    
    @staticmethod
    def get_by_client_id(client_id):
        """Busca um contato pelo CLIENT ID."""
        return db.session.query(Contact).filter_by(client_id=client_id).first()

    @staticmethod
    def create(validated_data):
        """Cria um novo contato."""
        new_contact = Contact(
            client_id=validated_data["client_id"],
            type_contact=validated_data["type_contact"],
            value_contact=validated_data["value_contact"]
            )
        db.session.add(new_contact)
        db.session.commit()
        db.session.refresh(new_contact)
        return new_contact
    
    @staticmethod
    def update(contact, new_data):
        """Atualiza um contato no banco de dados."""
        contact.client_id = new_data["client_id"]
        contact.type_contact = new_data["type_contact"]
        contact.value_contact = new_data["value_contact"]
        """Confirma as alterações no banco de dados."""
        db.session.commit()
        return contact

    @staticmethod
    def delete(contact):
        """Exclui um contato."""
        db.session.delete(contact)
        db.session.commit()
        return True
