from backend_app import db
from backend_app.models.client_model import Client
from backend_app.models.user_model import User
from backend_app.schemas.client_schema import ClientSchema
from datetime import datetime, timezone

def register_client(client_data):
    """Cadastrar um novo cliente."""
    user = User.query.filter_by(cpf=client_data["cpf"]).first()
    if not user:
        return {"error": "Usuário não encontrado"}, 400  

    new_client = Client(
        cpf=user.cpf,
        name=client_data["name"],
        register_date=datetime.now(timezone.utc)
    )
    db.session.add(new_client)
    db.session.commit()
    return ClientSchema().dump(new_client), 201  

def list_clients():
    """Listar todos os clientes."""
    clients = Client.query.all()
    return ClientSchema(many=True).dump(clients), 200  
def list_client_id(id):
    """Buscar um cliente pelo ID."""
    client = Client.query.get(id)
    if not client:
        return {"error": "Cliente não encontrado"}, 404 
    return ClientSchema().dump(client), 200  

def update_client(client_db, new_client_data):
    """Atualizar um cliente."""
    if not client_db:
        return {"error": "Cliente não encontrado"}, 404  

    client_db.name = new_client_data["name"]
    client_db.cpf = new_client_data["cpf"]
    db.session.commit()
    
    return ClientSchema().dump(client_db), 200 

def delete_client(client):
    """Excluir um cliente."""
    if isinstance(client, dict):  # 🔥 Se for dicionário, buscar o objeto real
        client = Client.query.get(client["id"])

    if not client:
        return {"error": "Cliente não encontrado"}, 404  

    db.session.delete(client)
    db.session.commit()
    
    return {"message": "Cliente deletado com sucesso"}, 204
