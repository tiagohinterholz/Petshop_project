from backend_app import db
from backend_app.models.user_model import User

class UserRepository:
    
    @staticmethod
    def get_by_email(email):
        """Busca um usuário pelo e-mail"""
        return db.session.query(User).filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_id(id):
        return db.session.get(User, id)
   
    @staticmethod
    def get_user_by_cpf(cpf):
        return db.session.query(User).filter_by(cpf=cpf).first()

    @staticmethod
    def list_all():
        """Lista todos Users."""
        return User.query.all()
    
    @staticmethod
    def create(validated_data):
        
        new_user = User(
            cpf=validated_data["cpf"], 
            name=validated_data["name"], 
            profile=validated_data["profile"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        new_user.encrypt_password()
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
    
    @staticmethod
    def update(user, new_data):
        """Atualiza um user no banco de dados."""

        # Atualiza apenas os campos enviados
        user.cpf = new_data.get("cpf", user.cpf)
        user.name = new_data.get("name", user.name)
        user.email = new_data.get("email", user.email)  # Adicionado para permitir atualização de e-mail
        user.profile = new_data.get("profile", user.profile)  # Caso precise permitir alteração de perfil

        # Atualiza a senha somente se estiver presente
        if "password" in new_data:
            user.password = new_data["password"]
            user.encrypt_password()  # Garante que a senha será armazenada corretamente

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
        
    
    