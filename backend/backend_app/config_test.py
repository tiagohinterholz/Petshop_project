import os

class TestConfig:
    """Configuração para ambiente de testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://test_user:test_password@localhost/petshop_test"  # PostgreSQL Teste
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "test_secret"
    
os.environ["FLASK_ENV"] = "testing"
os.environ["TESTING"] = "True"
