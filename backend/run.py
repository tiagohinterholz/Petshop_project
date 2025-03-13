import os
from backend_app import create_app

def dev():
    """Executa o servidor em modo desenvolvimento"""
    os.environ["FLASK_ENV"] = "development"
    os.environ["TESTING"] = "False"
    print("🚀 Rodando em modo DESENVOLVIMENTO...")
    app = create_app("development")
    app.run(debug=True)

def test():
    """Executa o servidor em modo de testes"""
    os.environ["FLASK_ENV"] = "testing"
    os.environ["TESTING"] = "True"
    print("🛠️ Rodando em modo de TESTE...")
    app = create_app("testing")
    app.run(debug=True)

if __name__ == "__main__":
    dev()  # Roda em modo desenvolvimento por padrão