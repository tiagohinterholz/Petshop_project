from backend_app import db
from backend_app.models.user_model import User, ProfileEnum

class UserRepository:
    @staticmethod
    def get_user_by_cpf(cpf):
        return db.session.query(User).filter_by(cpf=cpf).first()

    @staticmethod
    def list_all():
        """Lista todos Users."""
        return User.query.all()
    
    @staticmethod
    def create(validated_data):
        # Valida se o usuário está tentando criar um ADMIN
        if validated_data["profile"] == ProfileEnum.ADMIN:
            return {"error": "Não é permitido criar um usuário ADMIN via Rota API"}, 400
        
        new_user = User(
            cpf=validated_data["cpf"], 
            name=validated_data["name"], 
            profile=validated_data["profile"],
            password=validated_data["password"]
        )
        new_user.encrypt_password()
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
    
    @staticmethod
    def update(user, new_data):
        """Atualiza um user no banco de dados."""
        user.name = new_data.get("name", user.name)  # Evita erro se 'name' não vier
        
        if "password" in new_data:
            user.password = new_data["password"]
            user.encrypt_password()

        db.session.commit()
        return user
    
    @staticmethod
    def delete(user):
        """Exclui um user."""
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def update_password(user, new_password):
        """Atualiza a senha de um usuário com criptografia."""
        user.password = new_password
        user.encrypt_password()  # Corrige a falha de segurança
        db.session.commit()
        return user
        
    
    