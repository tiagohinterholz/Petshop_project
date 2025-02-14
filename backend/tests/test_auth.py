import unittest
from backend_app import app, db
from backend_app.models.user_model import User
from flask_jwt_extended import create_access_token

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial de cada teste"""
        self.app = app.test_client()
        self.db = db
        with app.app_context():
            self.db.create_all()
        
    def tearDown(self):
        """Limpar o BD após cada teste"""
        with app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_login_sucess(self):
        """Teste de um usuário fazendo login"""
        with app.app_context():
            user = User(cpf="12345678900", name="Admin", profile="ADMIN", password="senha123")
            user.encrypt_password()
            assert user.verify_password("senha123")  # <- Garante que a senha está sendo hasheada
            db.session.add(user)
            db.session.commit()
        
        response = self.app.post('/login', json={"cpf": "12345678900", "password": "senha123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)
    
    def test_login_fail(self):
        """Teste de falha de login com senha errada"""
        response = self.app.post('/login', json={"cpf": "12345678900", "password": "errada"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json)           

if __name__ == '__main__':
    unittest.main()