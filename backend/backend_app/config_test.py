import os
from dotenv import load_dotenv

load_dotenv()

class TestConfig:
    """Configuração para ambiente de testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:tiagotiago@localhost/petshop_test"  # PostgreSQL Teste
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    
os.environ["FLASK_ENV"] = "testing"
os.environ["TESTING"] = "True"
