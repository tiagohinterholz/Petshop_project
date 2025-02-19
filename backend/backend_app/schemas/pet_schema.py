from backend_app import ma 
from backend_app.models.pet_model import Pet
from marshmallow import fields, pre_load, post_load
from datetime import datetime

class PetSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Pet
        load_instance = True
        fields = ("id", "client_id", "breed_id", "birth_date", "name")

    client_id = fields.Integer(required=True)
    breed_id = fields.Integer(required=True)
    birth_date = fields.String(required=True)
    name = fields.String(required=True)

    @pre_load
    def process_birth_date(self, data, **kwargs):
        """Garante que o birth_date sempre vai como string válida"""
        print(f"\n[DEBUG] Antes da conversão: {data}")  
        
        if "birth_date" in data and isinstance(data["birth_date"], str):
            try:
                data["birth_date"] = datetime.strptime(data["birth_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de data inválido, use YYYY-MM-DD")
        
        print(f"[DEBUG] Depois da conversão: {data}")  
        return data

    @post_load
    def convert_birth_date(self, data, **kwargs):
        """Agora finalmente converte para `date` antes de ir pro banco"""
        if "birth_date" in data and isinstance(data["birth_date"], str):
            data["birth_date"] = datetime.strptime(data["birth_date"], "%Y-%m-%d").date()
        print(f"[DEBUG] Depois da validação: {data}")
        return data