from flask_jwt_extended import create_access_token, get_jwt_identity
from backend_app.models.user_model import User
from passlib.hash import pbkdf2_sha256
from datetime import timedelta

def authenticate_user(cpf, password):
    """Autentica o user verificando cpf e senha"""
    user = User.query.filter_by(cpf=cpf).first()
    
    if user and pbkdf2_sha256.verify(password, user.password):
        access_token = create_access_token(identity={"cpf": user.cpf, "profile": user.profile.value}, expires_delta=timedelta(hours=1))
        return access_token

    return None


def get_current_user():
    """Obtem user autenticado pelo token"""
    identity = get_jwt_identity()
    if not identity:
        return None
    return identity