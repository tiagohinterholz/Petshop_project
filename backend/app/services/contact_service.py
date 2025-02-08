from app import db
from app.models.contact_model import Contact
from app.models.client_model import Client

def register_contact(contact):
    
    client_exists = Client.query.get(contact.client_id)
    if not client_exists:    
        return None
    
    contact_db = Contact(client_id=contact.client_id,
                            type_contact=contact.type_contact,
                            value_contact=contact.value_contact
                        )
    db.session.add(contact_db)
    db.session.commit()
    return contact_db       

def list_contacts():
    return Contact.query.all()
    
def list_contact_id(id):
    return Contact.query.filter_by(id=id).first()

def update_contact(contact_db, new_contact):
    if not contact_db:
        return None
    contact_db.type_contact = new_contact.type_contact
    contact_db.value_contact = new_contact.value_contact
    db.session.commit()
    return contact_db

def delete_contact(contact):
    if not contact:
        return False
    db.session.delete(contact)
    db.session.commit()
    return True