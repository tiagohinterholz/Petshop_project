import unittest
from backend_app.models.user_model import User, ProfileEnum
from backend_app import create_app, db

class UserTestCase(unittest.TestCase):
    
    def setUp(self):
        """configuração inicial antes dos testes"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.admin_cpf = "000.000.000-00"
        self.admin_password = "admin123"
       
        # Criar um ADMIN fixo direto no banco
        with self.app.app_context():
            admin = db.session.query(User).filter_by(cpf=self.admin_cpf).first()
            if not admin:
                new_admin = User(
                    cpf=self.admin_cpf,
                    name="Admin Teste",
                    profile=ProfileEnum.ADMIN,
                    password=self.admin_password
                )
                new_admin.encrypt_password()  # Criptografa a senha antes de salvar
                db.session.add(new_admin)
                db.session.commit()
        
         
        """Testa se o admin consegue logar e pegar um token"""
        response = self.client.post('/login', json={
            "cpf": self.admin_cpf,
            "password": self.admin_password
        })
                
        data = response.get_json()
        if response.status_code != 200:
            print("Erro ao obter token! Resposta da API:", data)

        self.assertEqual(response.status_code, 200)  # Garante que o login foi bem-sucedido
        self.assertIn("access_token", data)  # Garante que o token foi retornado
        self.admin_token = data["access_token"]

        """Cria 3 usuários diferentes"""
        users = [
            {"cpf": "111.222.333-44", "name": "Usuário Um", "profile": "client", "password": "senha123"},
            {"cpf": "555.666.777-88", "name": "Usuário Dois", "profile": "client", "password": "senha123"},
            {"cpf": "999.000.111-22", "name": "Usuário Três", "profile": "client", "password": "senha123"}
        ]

        for user in users:
            response = self.client.post('/users', json=user, headers={
                "Authorization": f"Bearer {self.admin_token}"
            })
            data = response.get_json()
            print(f"📌 Criando usuário {user['cpf']} - Status: {response.status_code}, Resposta: {data}")  
                   
            self.assertEqual(response.status_code, 201, f"Erro ao criar usuário {user['cpf']}: {data}")
        
        """Testa se o client 1 consegue logar e pegar um token"""
        response = self.client.post('/login', json={
            "cpf": "111.222.333-44",
            "password": "senha123"
        })
        
        data = response.get_json()
        self.assertEqual(response.status_code, 200)  # Garante que o login foi bem-sucedido
        self.assertIn("access_token", data)  # Garante que o token foi retornado
        self.client_token = data["access_token"]
        
    def tearDown(self):
        """Remove todos os usuários criados nos testes"""
        with self.app.app_context():
            from backend_app.models.user_model import User  # Importando o model
            from backend_app import db  # Importando a conexão com o banco

            # Deletando todos os usuários de teste
            db.session.query(User).filter(User.cpf != self.admin_cpf).delete()
            db.session.commit()
        
    def test_get_all_users(self):
        """Testa a listagem de todos os usuários"""
        response = self.client.get('/users', headers={
            "Authorization": f"Bearer {self.admin_token}"
        })
        
        data = response.get_json()
        print(f"🔍 Usuários retornados: {data}")
        
        self.assertEqual(response.status_code, 200)  # Deve retornar 200 OK
        self.assertGreaterEqual(len(data), 3)  # Deve ter pelo menos 3 usuários cadastrados
    
    def test_get_user_by_cpf(self):
        """Testa a busca de um usuário pelo CPF"""
        cpf_teste = "111.222.333-44"  # Um dos CPFs cadastrados no teste anterior
        print(f"📌 Buscando usuário com CPF: {repr(cpf_teste)}")
               
        response = self.client.get(f'/users/{cpf_teste}', headers={
            "Authorization": f"Bearer {self.admin_token}"
        })

        data = response.get_json()

        print(f"📌 Resposta da API para GET /users/{cpf_teste}: {response.status_code}, {data}")
        
        self.assertEqual(response.status_code, 200)  # Deve retornar 200 OK
        self.assertEqual(data["cpf"], cpf_teste)  # O CPF deve ser o mesmo
    
    def test_update_user(self):
        """Testa a atualização dos dados de um usuário"""
        cpf_teste = "111.222.333-44"  # CPF de um usuário já cadastrado

        # Dados novos para atualização
        updated_data = {
            "cpf": cpf_teste,  # CPF pode ser obrigatório
            "name": "Usuário Atualizado",
            "profile": "client",  # Certifique-se de que o perfil está correto
            "password": "nova_senha123"
        }

        response = self.client.put(f'/users/{cpf_teste}', json=updated_data, headers={
            "Authorization": f"Bearer {self.admin_token}"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)  # Deve retornar 200 OK
        print(data["name"], "Usuário Atualizado")  # O nome deve estar atualizado

    def test_update_user_by_client(self):
        # CLIENT tenta atualizar um outro usuário (o admin, por exemplo)
        update_data = {"cpf": self.admin_cpf, "name": "Hacker Client", "profile": "admin", "password": "nova_senha123"}

        response = self.client.put(f'/users/{self.admin_cpf}', json=update_data, headers={
            "Authorization": f"Bearer {self.client_token}"
        })

        print(f"📌 Resposta ao tentar atualizar como CLIENT: {response.status_code}, {response.get_json()}")

        # Deve falhar com 403 Forbidden
        self.assertEqual(response.status_code, 403, "Client conseguiu alterar outro usuário!")     
    
if __name__ == "__main__":
    unittest.main()