from backend_app import ma
from backend_app.models.appointment_model import Appointment
from marshmallow import fields, pre_load, post_load
from datetime import datetime
class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Appointment
        load_instance = True
        fields = ("id", "pet_id", "desc_appoint", "price", "date_appoint")
    
    pet_id = fields.Integer(required=True)
    desc_appoint = fields.String(required=True)
    price = fields.Float(required=True)
    date_appoint = fields.String(required=True)
    
    @pre_load
    def process_date_appoint(self, data, **kwargs):
        """Garante que o date_appoint sempre vai como string válida"""
        print(f"\n[DEBUG] Antes da conversão: {data}")  
        
        if "date_appoint" in data and isinstance(data["date_appoint"], str):
            try:
                data["date_appoint"] = datetime.strptime(data["date_appoint"], "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de data inválido, use YYYY-MM-DD")
        
        print(f"[DEBUG] Depois da conversão: {data}")  
        return data

    @post_load
    def convert_date_appoint(self, data, **kwargs):
        """Agora finalmente converte para `date` antes de ir pro banco"""
        if "date_appoint" in data and isinstance(data["date_appoint"], str):
            data["date_appoint"] = datetime.strptime(data["date_appoint"], "%Y-%m-%d").date()
        print(f"[DEBUG] Depois da validação: {data}")
        return data