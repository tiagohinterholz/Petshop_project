from app import db
from app.models.user_model import User

def register_user(user):
    user_db = user_model.User(cpf=user.cpf, name=user.name, profile=user.profile, password=user.password)
    user_db.encrypt_password()
    db.session.add(user_db)
    db.session.commit()
    return user_db