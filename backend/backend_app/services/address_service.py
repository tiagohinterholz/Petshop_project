from backend_app import db
from backend_app.models.address_model import Address
from backend_app.schemas.address_schema import AddressSchema
from marshmallow import ValidationError

def list_addresses():
    """Lista todos os endereços cadastrados."""
    try:
        addresses = Address.query.all()
        return AddressSchema(many=True).dump(addresses), 200 
    except Exception as e:
        return {"error": f"Erro ao listar usuários: {str(e)}"}, 500

def register_address(address_data):
    """Cadastra um novo endereço para um cliente."""
    schema = AddressSchema()
    
    try:
        validated_data = schema.load(address_data)
    except ValidationError as err:
        return {"error": err.messages}, 400    
    
    address_db = Address(
        client_id=validated_data.client_id,
        street=validated_data.street,
        city=validated_data.city,
        neighborhood=validated_data.neighborhood,
        complement=validated_data.complement
    )

    try:
        db.session.add(address_db)
        db.session.commit()
        return schema.dump(address_db), 201
    except Exception as e:
        db.session.rollback()  # Evita inconsistências no banco
        return {"error": f"Erro ao cadastrar endereço: {str(e)}"}, 500 
    

def list_address_id(id):
    """Busca um endereço pelo ID."""
    try:
        address = db.session.get(Address, id)
        if not address:
            return {"error": "Endereço não encontrado"}, 404
        return AddressSchema().dump(address), 200  
    except Exception as e:
        return {"error": f"Erro ao buscar endereço: {str(e)}"}, 500
    
def update_address(address_db, new_address_data):
    """Atualiza um endereço existente."""
    if not address_db:
        return {"error": "Endereço não encontrado"}, 404

    try: 
        address_db.street = new_address_data["street"]
        address_db.city = new_address_data["city"]
        address_db.neighborhood = new_address_data["neighborhood"]
        address_db.complement = new_address_data["complement"]
        
        db.session.commit()
        return AddressSchema().dump(address_db), 200 
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao atualizar endereço: {str(e)}"}, 500
    
def delete_address(id):
    """Exclui um endereço."""
    try:
        address = db.session.get(Address, id)
        if not address:
            return {"error": "Endereço não encontrado"}, 404
        
        db.session.delete(address)
        db.session.commit()
        
        return {"message": "Endereço deletado com sucesso"}, 200  # Agora retorna um JSON

    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao excluir usuário: {str(e)}"}, 500
 
