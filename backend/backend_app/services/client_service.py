from backend_app import db
from backend_app.models.client_model import Client
from backend_app.models.user_model import User
from backend_app.models.user_model import ProfileEnum

def register_client(client):
    client_db = Client(name=client.name,
                      cpf=client.cpf,
                      register_date=client.register_date
                      )
    
    db.session.add(client_db)
    db.session.commit()
    
    # Criar usuário automaticamente com profile="client"
    user_db = User(
        cpf=client.cpf,
        name=client.name,
        profile=ProfileEnum.CLIENT,  # Forçar CLIENT
        password=hash_password(client.password)  # Precisamos de uma função para hash
    )

    db.session.add(user_db)
    db.session.commit()
        
    return client_db

def list_clients():
    return Client.query.all()
    
def list_client_id(id):
    client = Client.query.filter_by(id=id).first()
    if not client:
        return None
    return client

def update_client(client_db, new_client):
    if not client_db:
        return None
    client_db.name = new_client.name
    client_db.cpf = new_client.cpf
    client_db.register_date = new_client.register_date
    db.session.commit()
    return client_db

def delete_client(client):
    if not client:
        return None
    db.session.delete(client)
    db.session.commit()
    return True