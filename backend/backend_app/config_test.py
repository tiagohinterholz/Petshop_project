import os

class TestConfig:
    """Configuração para ambiente de testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usa SQLite em memória para testes rápidos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "test_secret")
    
os.environ["FLASK_ENV"] = "testing"
os.environ["TESTING"] = "True"