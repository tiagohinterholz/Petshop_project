from backend_app.models.user_model import User
from flask_jwt_extended import create_access_token, get_jwt_identity
from backend.backend_app.schema_dto.login_schema_dto import LoginSchema
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from backend_app import db

def authenticate_user(data):
    """Autentica o user verificando cpf e senha"""
    validation_errors = LoginSchema.validate_login(data)
    if validation_errors:
        return validation_errors
    
    cpf = data.get("cpf")
    password = data.get("password")
    
    # Buscar usuário no banco de dados
    user = db.session.query(User).filter_by(cpf=cpf).first()
    
    if not user or not pbkdf2_sha256.verify(password, user.password):
        return {"error": "CPF ou senha inválidos"}, 401
    
    # Gerar tokens JWT
    access_token = create_access_token(
        identity=str(user.cpf),
        additional_claims={"profile": user.profile.value},
        expires_delta=timedelta(hours=1)
    )
    
    return {"access_token": access_token}, 200

def get_current_user():
    """Obtem user autenticado pelo token"""
    identity = get_jwt_identity()
    if not identity:
        return {"error": "Usuário não autenticado"}, 400
    return identity