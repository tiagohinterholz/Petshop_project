from app import db
from app.models.address_model import Address
from app.models.client_model import Client

def register_address(address):
    
    client_exists = Client.query.get(address.client_id) # verifica se existe o client
    address_exists = Address.query.filter_by(client_id=address.client_id).first() # verifica se existe um address nele
    
    if not client_exists: # se não existe o cliente nao cadastra endereço   
        return None

    if address_exists: # se existe cliente e endereço não cadastrada novo endereço
        return None
    
    address_db = Address(
                    client_id=address.client_id,
                    street=address.street,
                    city=address.city,
                    neighborhood=address.neighborhood,
                    complement=address.complement
    )
    
    db.session.add(address_db)
    db.session.commit()
    return address_db 


def list_addresses():
    return Address.query.all()

def list_address_id(id):
    return Address.query.filter_by(id=id).first()

def update_address(address_db, new_address):
    if not address_db:
        return None
    address_db.street = new_address.street
    address_db.city = new_address.city
    address_db.neighborhood = new_address.neighborhood
    address_db.complement = new_address.complement
    db.session.commit()
    return address_db

def delete_address(address):
    if not address:
        return False
    db.session.delete(address)
    db.session.commit()
    return True