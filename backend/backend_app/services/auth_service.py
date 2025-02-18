from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token
from backend_app.models.user_model import User
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from flask import jsonify, make_response

def authenticate_user(cpf, password):
    """Autentica o user verificando cpf e senha"""
    user = User.query.filter_by(cpf=cpf).first()
    
    if user and pbkdf2_sha256.verify(password, user.password):
        access_token = create_access_token(
                identity=str(user.cpf),  # CPF como string
                additional_claims={"profile": user.profile.value},  # Informações extras
                expires_delta=timedelta(hours=1)
)       
        refresh_token = create_refresh_token(identity=str(user.cpf))
        
        return access_token, refresh_token

    return None


def get_current_user():
    """Obtem user autenticado pelo token"""
    identity = get_jwt_identity()
    if not identity:
        return {"error": "Usuário não autenticado"}, 400
    return identity