import unittest
from backend_app import create_app, db
from backend_app.schemas.contact_schema import ContactSchema
from backend_app.models.contact_model import ContactTypeEnum

class TestContactSchema(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Cria o contexto da aplicação para os testes"""
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Fecha o contexto da aplicação após os testes"""
        cls.app_context.pop()

    def test_contact_schema_serialization(self):
        schema = ContactSchema()
        data = {
            "id": 1,
            "client_id": 123,
            "type_contact": ContactTypeEnum.EMAIL,  # ENUM correto
            "value_contact": "example@email.com"
        }

        serialized_data = schema.dump(data)
        print("SERIALIZED:", serialized_data)
        
        self.assertEqual(serialized_data["client_id"], 123)
        self.assertEqual(serialized_data["type_contact"], "email")  # Agora verifica como string

    def test_contact_schema_deserialization(self):
        schema = ContactSchema()
        data = {
            "id": 1,
            "client_id": 123,
            "type_contact": "email",  # Agora está STRING, não ENUM
            "value_contact": "example@email.com"
        }

        deserialized_data = schema.load(data)
        print("DESERIALIZED:", deserialized_data)

        self.assertEqual(deserialized_data.client_id, 123)
        self.assertEqual(deserialized_data.type_contact, ContactTypeEnum.EMAIL)  # Agora comparando com ENUM

if __name__ == "__main__":
    unittest.main()
