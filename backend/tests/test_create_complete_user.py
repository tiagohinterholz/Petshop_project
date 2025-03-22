import unittest
from backend_app.models.user_model import User, ProfileEnum
from backend_app import create_app, db
from sqlalchemy import text
class CreateCompleteUser(unittest.TestCase):
    
    def setUp(self):
        """configuração inicial antes dos testes"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.admin_cpf = "000.000.000-00"
        self.admin_password = "admin123"
        self.admin_email = "fh.tiago@gmail.com"
       
        # Criar um ADMIN fixo direto no banco
        with self.app.app_context():
            admin = db.session.query(User).filter_by(cpf=self.admin_cpf).first()
            if not admin:
                new_admin = User(
                    cpf=self.admin_cpf,
                    name="Admin Teste",
                    profile=ProfileEnum.ADMIN,
                    password=self.admin_password,
                    email=self.admin_email
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
        
    def test_create_complete_client(self):
        #criar um usuário client para testar se ele completa todo o cadastro
        user = {
            "cpf": "222.222.333-44", 
            "name": "Usuário Um", 
            "profile": "client", 
            "password": "senha123",
            "email": "xx.tiago@gmail.com"
            }
        
        response = self.client.post("/users", json=user, headers={
            "Authorization": f"Bearer {self.admin_token}"})
     
        data = response.get_json()
        self.assertEqual(response.status_code, 201, f"Erro ao criar usuário: {data}")
        
        # agora vou logar com o user client e pegar o token pra começar o cadastro
        response = self.client.post('/login', json={
            "cpf": "222.222.333-44",
            "password": "senha123"
        })
        
        data = response.get_json()
        self.assertEqual(response.status_code, 200, f"Erro ao logar como client: {data}")  # Garante que o login foi bem-sucedido
        self.assertIn("access_token", data, "Token de acesso não retornado")  # Garante que o token foi retornado
        self.client_token = data["access_token"]
        
        client = {
            "cpf": user['cpf'],
        }
        
        response = self.client.post('/clients', json=client, headers={
            "Authorization": f"Bearer {self.client_token}"
        })
        client_data = response.get_json()
        self.assertEqual(response.status_code, 201, f"Erro ao criar cliente: {client_data}")
        #print(client_data)
        client_id = client_data.get("id")
        
        address = {
            "client_id": client_id,
            "street": "Rua Assis Brasil",
            "city": "Bento Gonçalves",
            "neighborhood": "São Francisco",
            "complement": "404"
        }
        response = self.client.post('/addresses', json=address, headers={
            "Authorization": f"Bearer {self.client_token}"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 201, f"Erro ao criar endereço: {data}")
        #print(f"Endereço cadastrado: {data}")
        
        contact = {
            "client_id": client_id,
            "type_contact": "email",
            "value_contact": "fh.tiago@gmail.com"
        }
        response = self.client.post('/contacts', json=contact, headers={
            "Authorization": f"Bearer {self.client_token}"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 201, f"Erro ao criar contato: {data}")
        #print(f"Contato cadastrado: {data}")
        
        breed = {"description": "Gato Siamês"}
        response = self.client.post('/breeds', json=breed, headers={
            "Authorization": f"Bearer {self.client_token}"
        })
        breed_data = response.get_json()
        breed_id = breed_data.get("id")
        print(breed_data)
        self.assertEqual(response.status_code, 201, f"Erro ao criar raça: {breed_data}")
        #print(f"Raça cadastrada: {breed_data}")
        
        pet = {"client_id": client_id,
               "breed_id": breed_id,
               "birth_date": "2016-10-13",
               "name": "Luna Baratto Hinterholz"
        }
        response = self.client.post('/pets', json=pet, headers={
            "Authorization": f"Bearer {self.client_token}"
        })
        pet_data = response.get_json()
        pet_id = pet_data.get("id")
        self.assertEqual(response.status_code, 201, f"Erro ao criar pet: {pet_data}")
        #print(f"Pet cadastrado: {pet_data}")
        
        appointment = {
            "pet_id": pet_id,
            "desc_appoint": "Banho e tosa na molenga",
            "price": "500",
            "date_appoint": "2025-04-30"
        }        
        response = self.client.post('/appointments', json=appointment, headers={
            "Authorization": f"Bearer {self.client_token}"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 201, f"Erro ao criar agendamento: {data}")
        #print(f"Agendamento cadastrado: {data}")
        
        response = self.client.post('/forgot-password', json={"email": "fh.tiago@gmail.com"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200, "Erro ao gerar token de reset de password")

        reset_token = data.get("reset_token")
        self.assertIsNotNone(reset_token, "Token de reset não retornado.")

        response = self.client.post('/reset-password', json={"token": reset_token, "new_password": "novaSenha123"})
        data = response.get_json()
        print(f"🔍 Resposta do reset-password: {data}")  # Adiciona um print para depuração
        self.assertEqual(response.status_code, 200, "Erro ao redefinir senha.")
        
    def tearDown(self):
        with self.app.app_context():
            from backend_app.models.password_reset_model import PasswordReset
            from backend_app.models.breed_model import Breed
            from backend_app.models.appointment_model import Appointment
            from backend_app.models.pet_model import Pet
            from backend_app.models.address_model import Address        
            from backend_app.models.contact_model import Contact
            from backend_app.models.client_model import Client
            from backend_app.models.user_model import User
            from backend_app import db  # Importando a conexão com o banco
            
            # Deletando todos os dados de teste
            db.session.query(PasswordReset).delete()
            db.session.query(Appointment).delete()
            db.session.query(Pet).delete()                       
            db.session.query(Address).delete()                     
            db.session.query(Contact).delete()
            db.session.query(Client).delete()
            db.session.query(Breed).delete()
            db.session.query(User).delete()
            db.session.commit()
            
            # 🔄 Resetando IDs das tabelas (PostgreSQL)

            def reset_sequence(seq_name):
                db.session.execute(text(f"ALTER SEQUENCE {seq_name} RESTART WITH 1"))
            
            #reset_sequence("passwordreset_id_seq")
            reset_sequence("appointment_id_seq")
            reset_sequence("pet_id_seq")
            reset_sequence("address_id_seq")
            reset_sequence("contact_id_seq")
            reset_sequence("client_id_seq")
            reset_sequence("breed_id_seq")
            db.session.commit()
     
if __name__ == "__main__":
    unittest.main()