from backend_app import db
from backend_app.models.contact_model import Contact
from backend_app.models.client_model import Client
from backend_app.schemas.contact_schema import ContactSchema 

def register_contact(contact_data):
    """Cadastra um novo contato."""
    client_exists = Client.query.get(contact_data["client_id"])
    if not client_exists:    
        return {"error": "Cliente não encontrado"}, 400
    
    contact_db = Contact(
        client_id=contact_data["client_id"],
        type_contact=contact_data["type_contact"],
        value_contact=contact_data["value_contact"]
    )
    db.session.add(contact_db)
    db.session.commit()
    
    return ContactSchema().dump(contact_db), 201 

def list_contacts():
    """Lista todos os contatos."""
    contacts = Contact.query.all()
    return ContactSchema(many=True).dump(contacts), 200

def list_contact_id(id):
    """Busca um contato pelo ID."""
    contact = Contact.query.get(id)
    if not contact:
        return {"error": "Contato não encontrado"}, 404
    return ContactSchema().dump(contact), 200  

def update_contact(contact_db, new_contact_data):
    """Atualiza um contato."""
    if not contact_db:
        return {"error": "Contato não encontrado"}, 404  

    contact_db.type_contact = new_contact_data["type_contact"]
    contact_db.value_contact = new_contact_data["value_contact"]
    db.session.commit()
    
    return ContactSchema().dump(contact_db), 200

def delete_contact(contact):
    """Exclui um contato."""
    if not contact:
        return {"error": "Contato não encontrado"}, 404  

    db.session.delete(contact)
    db.session.commit()
    
    return {}, 204 
