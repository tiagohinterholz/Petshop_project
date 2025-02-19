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
    with app.app_context():
        return create_access_token(identity="44445678911", additional_claims={"profile": "client"}, expires_delta=timedelta(hours=1))

def test_client_registration_and_operations(client, client_token):
     
    with app.app_context():
        try:
            headers = {"Authorization": f"Bearer {client_token}"}

            # 1️⃣ Cadastrar um novo usuário (client)
            user_response = client.post("/users", json={
                "cpf": "44445678911",
                "name": "User Test",
                "password": "123456",
                "profile": "client"
            })
            print("\n[DEBUG] Cadastro usuário - Status:", user_response.status_code, "Response:", user_response.get_json())

            assert user_response.status_code == 201
            user_data = user_response.get_json()
            assert user_data["cpf"] == "44445678911"

            # 2️⃣ Criar um CLIENTE vinculado ao usuário (CPF -> ID)
            client_response = client.post("/clients", json={
                "name": "Cliente Teste",
                "cpf": user_data["cpf"]
            }, headers=headers)
            print("\n[DEBUG] Cadastro cliente - Status:", client_response.status_code, "Response:", client_response.get_json())

            assert client_response.status_code == 201
            client_data = client_response.get_json()
            assert client_data["cpf"] == "44445678911"
            client_id = client_data["id"]
            print("[DEBUG] Cliente ID:", client_id)

            # 3️⃣ Criar um endereço para o CLIENTE
            address_response = client.post("/addresses", json={
                "client_id": client_id,
                "street": "Rua Teste",
                "city": "Cidade Teste",
                "neighborhood": "Bairro Teste",
                "complement": "Apto 101"
            }, headers=headers)
            print("\n[DEBUG] Cadastro endereço - Status:", address_response.status_code, "Response:", address_response.get_json())

            assert address_response.status_code == 201

            # 4️⃣ Criar um contato para o CLIENTE
            contact_response = client.post("/contacts", json={
                "client_id": client_id,
                "type_contact": "email",
                "value_contact": "cliente@email.com"
            }, headers=headers)
            print("\n[DEBUG] Cadastro contato - Status:", contact_response.status_code, "Response:", contact_response.get_json())

            assert contact_response.status_code == 201

            # 5️⃣ Criar uma raça
            breed_response = client.post("/breeds", json={
                "description": "Golden Retriever"
            }, headers=headers)
            print("\n[DEBUG] Cadastro raça - Status:", breed_response.status_code, "Response:", breed_response.get_json())

            assert breed_response.status_code == 201
            breed_data = breed_response.get_json()
            breed_id = breed_data["id"]
            print("[DEBUG] Raça ID:", breed_id)
            
            # 6️⃣ Criar um pet associado ao CLIENTE e à RAÇA
            pet_data = {
                "client_id": client_id,
                "breed_id": breed_id,
                "birth_date": '2022-01-01',  # Garantindo que está como string
                "name": "Rex"
            }
            print("\n[DEBUG] Tipo de birth_date antes do POST:", type(pet_data["birth_date"]))  # Deve ser <class 'str'>


            pet_response = client.post("/pets", json=pet_data, headers=headers)
            print("\n[DEBUG] Cadastro pet - Status:", pet_response.status_code, "Response:", pet_response.data.decode("utf-8"))

            assert pet_response.status_code == 201
            pet_data = pet_response.get_json()
            pet_id = pet_data["id"]
            print("[DEBUG] Pet ID:", pet_id)

            # 7️⃣ Criar um agendamento para o PET
            appointment_response = client.post("/appointments", json={
                "pet_id": pet_id,
                "desc_appoint": "Banho e tosa",
                "price": 100.0,
                "date_appoint": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            }, headers=headers)
            print("\n[DEBUG] Cadastro agendamento - Status:", appointment_response.status_code, "Response:", appointment_response.get_json())

            assert appointment_response.status_code == 201

        except Exception as e:
            db.session.rollback()
            print("\n[ERROR] Ocorreu um erro durante o teste:", str(e))
            raise e
