from backend_app import db
from backend_app.models.user_model import User, ProfileEnum

class UserRepository:
    
   
    
    def validate_profile(self, value):
        if value == ProfileEnum.ADMIN:
            raise Exception ("Não é permitido criar um usuário ADMIN")
    
    def get_user_by_cpf(cpf):
        return db.session.query(User).filter_by(cpf=cpf).first()