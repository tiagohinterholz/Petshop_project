from backend_app import db
from backend_app.models.contact_model import Contact
from backend_app.models.client_model import Client
from backend.backend_app.repository.contact_repository import ContactSchema 
from marshmallow import ValidationError

def list_contacts():
    """Lista todos os contatos."""
    try:
        contacts = Contact.query.all()
        return ContactSchema(many=True).dump(contacts), 200
    except Exception as e:
        return {'error': f'Erro ao listar contatos: {e}'}, 500
        
def register_contact(contact_data):
    """Cadastra um novo contato."""
    
    schema = ContactSchema()
    
    try:
        validated_data = schema.load(contact_data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    
    
    try: 
        contact_db = Contact(
            client_id=validated_data.client_id,
            type_contact=validated_data.type_contact,
            value_contact=validated_data.value_contact
        )
        db.session.add(contact_db)
        print("[DEBUG] Salvando contato no banco:", contact_db)
        db.session.commit()  
        return ContactSchema().dump(contact_db), 201 
    except Exception as e:
        db.session.rollback()  # Evita inconsistências no banco
        return {"error": f"Erro ao cadastrar contato: {str(e)}"}, 500
        
def list_contact_id(id):
    """Busca um contato pelo ID."""
    try:
        contact = db.session.get(Contact, id)
        if not contact:
            return {"error": "Contato não encontrado"}, 404
        return ContactSchema().dump(contact), 200  
    except Exception as e:
        return {"error": f"Erro ao buscar contato: {str(e)}"}, 500
        
def update_contact(contact_db, new_contact_data):
    """Atualiza um contato."""
    if not contact_db:
        return {"error": "Contato não encontrado"}, 404  

    try:
        contact_db.type_contact = new_contact_data["type_contact"]
        contact_db.value_contact = new_contact_data["value_contact"]
        db.session.commit()  
        return ContactSchema().dump(contact_db), 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao atualizar contato: {e}"}

def delete_contact(id):
    """Exclui um contato."""
    try:
        contact = db.session.get(Contact, id)
        if not contact:
            return {"error": "Contato não encontrado"}, 404  

        db.session.delete(contact)
        db.session.commit()
        return {"message": "Contato deletado com sucesso"}, 200
    except Exception as e: 
        db.session.rollback()
        return {"error": f"Erro ao deletar contato: {e}"}, 500 
