import pytest
from datetime import datetime, timedelta


def test_client_registration_and_operations(client, client_token):
    import pytest

def test_client_registration_and_operations(test_client, test_db, client_token):
    """Testa o cadastro de um cliente e suas operações básicas"""
    
    headers = {"Authorization": f"Bearer {client_token}"}

    # 1️⃣ Cadastrar um novo usuário (perfil client)
    user_response = test_client.post("/users", json={
        "cpf": "44445678911",
        "name": "User Test",
        "password": "123456",
        "profile": "client"
    })
    assert user_response.status_code == 201
    user_data = user_response.get_json()
    assert user_data["cpf"] == "44445678911"

    # 2️⃣ Criar um CLIENTE vinculado ao usuário (CPF -> ID)
    client_response = test_client.post("/clients", json={
        "name": "Cliente Teste",
        "cpf": user_data["cpf"],
        "register_date": "2024-01-01"
    }, headers=headers)
    print("\n[DEBUG] Resposta ao criar cliente:", client_response.status_code, client_response.get_json())  # Adiciona debug
    assert client_response.status_code == 201
    client_data = client_response.get_json()
    assert client_data["cpf"] == "44445678911"
    client_id = client_data["id"]

    # 3️⃣ Criar um contato para o CLIENTE
    contact_response = test_client.post("/contacts", json={
        "client_id": client_id,
        "type_contact": "telefone",
        "value_contact": "cliente@email.com"
    }, headers=headers)
    print("[DEBUG] Resposta do servidor:", contact_response.status_code, contact_response.get_json())

    assert contact_response.status_code == 201


    # 5️⃣ Criar uma raça
    breed_response = test_client.post("/breeds", json={
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


    pet_response = test_client.post("/pets", json=pet_data, headers=headers)
    print("\n[DEBUG] Cadastro pet - Status:", pet_response.status_code, "Response:", pet_response.data.decode("utf-8"))

    assert pet_response.status_code == 201
    pet_data = pet_response.get_json()
    pet_id = pet_data["id"]
    print("[DEBUG] Pet ID:", pet_id)

    # 7️⃣ Criar um agendamento para o PET
    appointment_response = test_client.post("/appointments", json={
        "pet_id": pet_id,
        "desc_appoint": "Banho e tosa",
        "price": 100.0,
        "date_appoint": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    }, headers=headers)
    print("\n[DEBUG] Cadastro agendamento - Status:", appointment_response.status_code, "Response:", appointment_response.get_json())

    assert appointment_response.status_code == 201