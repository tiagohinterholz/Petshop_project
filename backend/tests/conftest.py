import pytest
import os
from backend_app import create_app, db
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='session')
def test_app():
    """Configura a aplicação para testes e conecta ao PostgreSQL de testes."""
    app = create_app()
    os.environ["TESTING"] = "True"  # Garante que a configuração de testes seja carregada
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://test_user:senha@localhost/petshop_test"
    
    with app.app_context():
        yield app  # Retorna a aplicação para uso nos testes

@pytest.fixture(scope="session")
def test_db(test_app):
    """Recria o banco de testes no PostgreSQL antes de cada sessão de testes."""
    with test_app.app_context():
        db.drop_all()  # Apaga tudo para evitar sujeira
        db.create_all()  # Recria todas as tabelas
        yield db
        db.session.remove()
        db.drop_all()  # Garante que o banco será limpo após os testes

@pytest.fixture(scope='session')
def test_client(test_app):
    """Cria um cliente de teste para fazer requisições"""
    return test_app.test_client()

@pytest.fixture(scope="function")
def admin_token():
    """Cria um token de admin válido para autenticação."""
    return create_access_token(identity="admin", additional_claims={"cpf": "admin", "profile": "admin"}, expires_delta=False)

@pytest.fixture(scope="function")
def client_token():
    """Cria um token de cliente válido para autenticação."""
    return create_access_token(identity="44445678911", additional_claims={"cpf": "44445678911", "profile": "client"}, expires_delta=False)
