import pytest
from backend_app.models.user_model import User

def test_login_success(test_client, test_db):
    """Teste de um usuário fazendo login com sucesso"""
    with test_client.application.app_context():
        user = User(cpf="12345678900", name="Admin", profile="ADMIN", password="senha123")
        user.encrypt_password()
        assert user.verify_password("senha123")
        test_db.session.add(user)
        test_db.session.commit()
    
    response = test_client.post('/login', json={"cpf": "12345678900", "password": "senha123"})
    assert response.status_code == 200
    assert "access_token" in response.json

def test_login_fail(test_client):
    """Teste de falha de login com senha errada"""
    response = test_client.post('/login', json={"cpf": "12345678900", "password": "errada"})
    assert response.status_code == 401
    assert "error" in response.json