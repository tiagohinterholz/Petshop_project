from backend_app import db
from backend_app.models.client_model import Client
from backend_app.schemas.client_schema import ClientSchema
from datetime import datetime, timezone
from marshmallow import ValidationError

def list_clients():
    """Listar todos os clientes."""
    try:
        clients = Client.query.all()
        return ClientSchema(many=True).dump(clients), 200  
    except Exception as e:
        return {'error': f'Erro ao listar clientes: {e}'}, 500

def register_client(client_data):
    """Cadastrar um novo cliente."""
    
    schema = ClientSchema()
    
    try:
        validated_data = schema.load(client_data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    
    new_client = Client(
        cpf=validated_data['cpf'],
        name=validated_data["name"],
        register_date=datetime.now(timezone.utc)
    )
    try:
        db.session.add(new_client)
        db.session.commit()
        return schema.dump(new_client), 201 
    except Exception as e:
        db.session.rollback()  # Evita inconsistências no banco
        return {"error": f"Erro ao cadastrar cliente: {str(e)}"}, 500 

def list_client_id(id):
    """Buscar um cliente pelo ID."""
    try:
        client = db.session.get(Client, id)
        if not client:
            return {"error": "Cliente não encontrado"}, 404 
        return ClientSchema().dump(client), 200
    except Exception as e:
        return {"error": f"Erro ao buscar cliente: {str(e)}"}, 500
        
def update_client(client_db, new_client_data):
    """Atualizar um cliente."""
    if not client_db:
        return {"error": "Cliente não encontrado"}, 404  

    try:
        client_db.name = new_client_data["name"]
        client_db.cpf = new_client_data["cpf"]
        db.session.commit()
        return ClientSchema().dump(client_db), 200 
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao atualizar cliente: {str(e)}"}, 500
        
def delete_client(id):
    """Excluir um cliente."""
    try:
        client = db.session.get(Client, id)
        if not client:
            return {"error": "Cliente não encontrado"}, 404  

        db.session.delete(client)
        db.session.commit()
        return {"message": "Cliente deletado com sucesso"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao excluir cliente: {str(e)}"}, 500
 