from backend_app import db
from backend_app.models.user_model import User


def list_users():
    """Retorna todos os usuários cadastrados"""
    return User.query.all()


def register_user(user):
    #verifica se o cpf já existe
    existing_user = User.query.get(user.cpf)
    if existing_user:
        return None
    
    user_db = User(cpf=user.cpf, name=user.name, profile=user.profile, password=user.password)
    user_db.encrypt_password()
    db.session.add(user_db)
    db.session.commit()
    return user_db

def list_user_id(cpf):
    return User.query.filter_by(cpf=cpf).first()

def update_user(user_db, new_user):
    user_db.name = new_user.name
    user_db.password = new_user.password  # Aqui já estará encriptada no schema
    db.session.commit()
    return user_db

def delete_user(cpf):
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True