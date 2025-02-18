import pytest
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from backend_app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.rollback()

@pytest.fixture
def client_token():
    """Gera um token JWT válido para um usuário com perfil 'client'"""
    with app.app_context():  # ✅ Garante que está dentro do contexto
        return create_access_token(identity="22345678911", additional_claims={"profile": "client"}, expires_delta=timedelta(hours=1))

def test_client_registration_and_operations(client, client_token):
    headers = {"Authorization": f"Bearer {client_token}"}

    # 1️⃣ Cadastrar um novo usuário (client)
    user_response = client.post("/users", json={
        "cpf": "22345678911",
        "name": "User Test",
        "password": "123456",
        "profile": "client"
    })
    
    if user_response.status_code == 400:
        print("Erro ao cadastrar usuário:", user_response.get_json())  # 🔥 Debug
    
    assert user_response.status_code == 201
    user_data = user_response.get_json()
    assert user_data["cpf"] == "22345678911"

    # 2️⃣ Criar um CLIENTE vinculado ao usuário (CPF -> ID)
    client_response = client.post("/clients", json={
        "name": "Cliente Teste",
        "cpf": user_data["cpf"]
    }, headers=headers)
    assert client_response.status_code == 201
    client_data = client_response.get_json()
    assert client_data["cpf"] == "22345678911"
    client_id = client_data["id"]  # PEGANDO O ID DO CLIENTE ✅

    # 3️⃣ Criar um endereço para o CLIENTE (usando client_id)
    address_response = client.post("/address", json={
        "client_id": client_id,  # AGORA USA O ID DO CLIENTE ✅
        "street": "Rua Teste",
        "city": "Cidade Teste",
        "neighborhood": "Bairro Teste",
        "complement": "Apto 101"
    }, headers=headers)
    assert address_response.status_code == 201
    address_data = address_response.get_json()
    assert address_data["street"] == "Rua Teste"

    # 4️⃣ Criar um contato para o CLIENTE (usando client_id)
    contact_response = client.post("/contacts", json={
        "client_id": client_id,  # AGORA USA O ID DO CLIENTE ✅
        "type_contact": "email",
        "value_contact": "cliente@email.com"
    }, headers=headers)
    assert contact_response.status_code == 201
    contact_data = contact_response.get_json()
    assert contact_data["type_contact"] == "email"

    # 5️⃣ Criar uma raça
    breed_response = client.post("/breeds", json={
        "description": "Golden Retriever"
    }, headers=headers)
    assert breed_response.status_code == 201
    breed_data = breed_response.get_json()
    assert breed_data["description"] == "Golden Retriever"
    breed_id = breed_data["id"]  # PEGANDO O ID DA RAÇA ✅

    # 6️⃣ Criar um pet associado ao CLIENTE e à RAÇA
    pet_response = client.post("/pets", json={
        "client_id": client_id,  # AGORA USA O ID DO CLIENTE ✅
        "breed_id": breed_id,  # VINCULA COM A RAÇA
        "birth_date": "2022-01-01",
        "name": "Rex"
    }, headers=headers)
    assert pet_response.status_code == 201
    pet_data = pet_response.get_json()
    assert pet_data["name"] == "Rex"
    pet_id = pet_data["id"]  # PEGANDO O ID DO PET ✅

    # 7️⃣ Criar um agendamento para o PET
    appointment_response = client.post("/appointments", json={
        "pet_id": pet_id,  # AGORA USA O ID DO PET ✅
        "desc_appoint": "Banho e tosa",
        "price": 100.0,
        "date_appoint": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    }, headers=headers)
    assert appointment_response.status_code == 201
    appointment_data = appointment_response.get_json()
    assert appointment_data["desc_appoint"] == "Banho e tosa"
