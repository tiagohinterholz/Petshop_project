from backend_app import db
from backend_app.models.address_model import Address
from backend_app.models.client_model import Client
from backend_app.schemas.address_schema import AddressSchema

def register_address(address_data):
    """Cadastra um novo endereço para um cliente."""
    client_exists = Client.query.get(address_data["client_id"])
    address_exists = Address.query.filter_by(client_id=address_data["client_id"]).first()

    if not client_exists:  
        return {"error": "Cliente não encontrado"}, 404 

    if address_exists:  
        return {"error": "Este cliente já possui um endereço cadastrado"}, 400 
    
    address_db = Address(
        client_id=address_data["client_id"],
        street=address_data["street"],
        city=address_data["city"],
        neighborhood=address_data["neighborhood"],
        complement=address_data["complement"]
    )
    
    db.session.add(address_db)
    db.session.commit()
    
    return AddressSchema().dump(address_db), 201

def list_addresses():
    """Lista todos os endereços cadastrados."""
    addresses = Address.query.all()
    return AddressSchema(many=True).dump(addresses), 200 

def list_address_id(id):
    """Busca um endereço pelo ID."""
    address = Address.query.get(id)
    if not address:
        return {"error": "Endereço não encontrado"}, 404
    return AddressSchema().dump(address), 200  

def update_address(address_db, new_address_data):
    """Atualiza um endereço existente."""
    if not address_db:
        return {"error": "Endereço não encontrado"}, 404

    address_db.street = new_address_data["street"]
    address_db.city = new_address_data["city"]
    address_db.neighborhood = new_address_data["neighborhood"]
    address_db.complement = new_address_data["complement"]
    
    db.session.commit()
    
    return AddressSchema().dump(address_db), 200 

def delete_address(address):
    """Exclui um endereço."""
    if not address:
        return {"error": "Endereço não encontrado"}, 404

    db.session.delete(address)
    db.session.commit()
    
    return {}, 204  # ✅ Correção: `204 No Content` para deleções
