import pytest
from flask_jwt_extended import create_access_token
from backend_app import api, db


def test_admin_can_delete_client(test_client, test_db, admin_token):
    """Testa se um admin pode deletar um cliente"""
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Criar usuário
    user_response = test_client.post("/users", json={
        "cpf": "12345678901",
        "name": "User Test",
        "password": "123456",
        "profile": "client"
    }, headers=headers)
    assert user_response.status_code == 201
    user_data = user_response.get_json()
    user_cpf = user_data.get("cpf")

    # Criar cliente vinculado
    client_response = test_client.post("/clients", json={
        "name": "Cliente Teste",
        "cpf": user_cpf,
        "register_date": "2025-01-01"
    }, headers=headers)
    print("\n[DEBUG] Resposta ao criar cliente:", client_response.status_code, client_response.get_json())  # Adiciona debug
    assert client_response.status_code == 201
    client_id = client_response.get_json().get("id")
    assert client_id is not None
    
    print("[DEBUG] Buscando cliente antes de deletar...")
    get_client_response = test_client.get(f"/clients/{client_id}", headers=headers)
    print("[DEBUG] Resposta do GET:", get_client_response.status_code, get_client_response.get_json())
    
    # Deletar cliente
    print("[DEBUG] Tentando deletar cliente com ID:", client_id)
    delete_response = test_client.delete(f"/clients/{client_id}", headers=headers)
    assert delete_response.status_code == 200
    print("[DEBUG] Resposta ao deletar:", delete_response.status_code, delete_response.get_json())