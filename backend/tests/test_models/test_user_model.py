from backend_app import create_app, db
from backend_app.models.user_model import User, ProfileEnum
from backend_app.models.client_model import Client

app = create_app()

with app.app_context():
    # Criar um cliente primeiro
    new_client = Client(id=1, cpf="12345678900", name="John Doe", register_date="2025-01-01")
    db.session.add(new_client)
    db.session.commit()
    
    # Criar um user agora
    new_user = User(cpf="12345678900", name="John Doe", profile=ProfileEnum.CLIENT, password="hashedpassword")
    db.session.add(new_user)
    db.session.commit()
    print("Usuário criado com sucesso!")
    