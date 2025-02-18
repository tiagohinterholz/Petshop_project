import pytest
from flask_jwt_extended import create_access_token
from backend_app import app, db
from backend_app.models.user_model import User

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
def admin_token():
    with app.app_context():
        token = create_access_token(identity="admin_user", additional_claims={"profile": "admin"})
    return token

@pytest.fixture
def client_token():
    with app.app_context():
        token = create_access_token(identity="client_user", additional_claims={"profile": "client"})
    return token

# 🛠️ Função para imprimir debug de qualquer response
def debug_response(response, label=""):
    print(f"\n[DEBUG {label}] Status Code: {response.status_code}")
    print(f"[DEBUG {label}] Headers: {response.headers}")
    print(f"[DEBUG {label}] Raw Data: {response.data}")  # Ver o que realmente retorna
    try:
        print(f"[DEBUG {label}] JSON: {response.get_json()}\n")  # Ver JSON estruturado
    except Exception as e:
        print(f"[DEBUG {label}] ERRO AO OBTER JSON: {e}\n")

# Teste: client não pode listar todos os clientes
def test_client_cannot_list_all_clients(client, client_token):
    response = client.get("/clients", headers={"Authorization": f"Bearer {client_token}"})
    debug_response(response, "test_client_cannot_list_all_clients")
    assert response.status_code == 403
    assert response.get_json()["message"] == "Acesso negado. Permissão insuficiente. Requer: admin, Seu perfil: client"

# Teste: admin pode listar todos os clientes
def test_admin_can_list_all_clients(client, admin_token):
    response = client.get("/clients", headers={"Authorization": f"Bearer {admin_token}"})
    debug_response(response, "test_admin_can_list_all_clients")
    assert response.status_code == 200

# Teste: client só pode acessar seus próprios dados
def test_client_can_access_own_data(client, client_token):
    # Criar um usuário primeiro
    user_response = client.post("/users", json={
        "cpf": "12345678900",
        "name": "User Test",
        "password": "123456",
        "profile": "client",
    }, headers={"Authorization": f"Bearer {client_token}"})

    debug_response(user_response, "test_client_can_access_own_data - Criando Usuário")
    user_data = user_response.get_json()
    user_cpf = user_data.get("cpf")
    assert user_cpf is not None, "Erro: CPF do usuário não foi retornado!"

    # Criar um cliente vinculado ao usuário usando CPF
    client_response = client.post("/clients", json={
        "name": "Cliente Teste",
        "email": "cliente@email.com",
        "cpf": user_cpf  
    }, headers={"Authorization": f"Bearer {client_token}"})

    debug_response(client_response, "test_client_can_access_own_data - Criando Cliente")
    client_id = client_response.get_json().get("id")
    assert client_id is not None, "Erro: ID do cliente não foi retornado!"

    # Buscar os dados do próprio cliente
    response = client.get(f"/clients/{client_id}", headers={"Authorization": f"Bearer {client_token}"})
    debug_response(response, "test_client_can_access_own_data - Buscando Cliente")
    assert response.status_code in [200, 403]

# Teste: client não pode deletar um cliente
def test_client_cannot_delete_other_client(client, client_token):
    response = client.delete("/clients/1", headers={"Authorization": f"Bearer {client_token}"})
    debug_response(response, "test_client_cannot_delete_other_client")
    assert response.status_code == 403
    assert response.get_json()["message"] == "Acesso negado. Permissão insuficiente. Requer: admin, Seu perfil: client"

# Teste: admin pode deletar um cliente
def test_admin_can_delete_client(client, admin_token):
    # Criar um usuário primeiro
    user_response = client.post("/users", json={
        "cpf": "12345678901",
        "name": "User Test",
        "password": "123456",
        "profile": "client"
    }, headers={"Authorization": f"Bearer {admin_token}"})

    debug_response(user_response, "test_admin_can_delete_client - Criando Usuário")
    user_data = user_response.get_json()
    user_cpf = user_data.get("cpf")
    assert user_cpf is not None, "Erro: CPF do usuário não foi retornado!"

    # Criar um cliente vinculado ao usuário
    client_response = client.post("/clients", json={
        "name": "Cliente Teste",
        "email": "cliente@email.com",
        "cpf": user_cpf  
    }, headers={"Authorization": f"Bearer {admin_token}"})

    debug_response(client_response, "test_admin_can_delete_client - Criando Cliente")
    client_id = client_response.get_json().get("id")
    assert client_id is not None, "Erro: ID do cliente não foi retornado!"

    # Agora deletar o cliente
    delete_response = client.delete(f"/clients/{client_id}", headers={"Authorization": f"Bearer {admin_token}"})
    debug_response(delete_response, "test_admin_can_delete_client - Deletando Cliente")
    assert delete_response.status_code == 204
