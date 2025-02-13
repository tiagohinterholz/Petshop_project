from backend_app import db
from backend_app.models.user_model import User

def register_user(user):
    user_db = User(cpf=user.cpf, name=user.name, profile=user.profile, password=user.password)
    user_db.encrypt_password()
    db.session.add(user_db)
    db.session.commit()
    return user_db

def list_user_id(cpf):
    return User.query.filter_by(cpf=cpf).first()

def delete_user(cpf):
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True