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
    def create(validated_data):
        """Cria um novo contato."""
        new_contact = Contact(
            contact_id=validated_data["contact_id"],
            type_contact=validated_data["type_contact"],
            value_contact=validated_data["value_contact"]
            )
        db.session.add(new_contact)
        db.session.commit()
        return new_contact
    
    @staticmethod
    def update(contact, new_data):
        """Atualiza um contato no banco de dados."""
        contact.contact_id = new_data["contact_id"],
        contact.type_contact = new_data["type_contact"],
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
