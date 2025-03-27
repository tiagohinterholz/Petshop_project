from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token
from backend_app.repository.user_repository import UserRepository
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from backend_app.utils.formatar_cpf import formatar_cpf

def authenticate_user(data):
    """Autentica o user verificando cpf e senha"""
    cpf = formatar_cpf(data.get("cpf"))
    password = data.get("password")
    
    if not cpf or not password:
        return {"error": "CPF e senha são obrigatórios"}, 400
    
    # Buscar usuário no banco de dados
    user = UserRepository.get_user_by_cpf(cpf)
    
    if not user or not pbkdf2_sha256.verify(password, user.password):
        return {"error": "CPF ou senha inválidos"}, 401
    
    # Gerar tokens JWT
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"profile": user.profile.value},
        expires_delta=timedelta(hours=1)
    )
    
    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=timedelta(days=7)  # Refresh token dura mais tempo
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }, 200

def get_current_user():
    """Obtem user autenticado pelo token"""
    cpf = get_jwt_identity()
    if not cpf:
        return {"error": "Usuário não autenticado"}, 401
    
    user = UserRepository.get_user_by_cpf(cpf)
    if not user:
        return {"error": "Usuário não encontrado"}, 404
        
    return {"id": user.id,
            "cpf": user.cpf,
            "nome": user.name,
            "perfil": user.profile.value}, 200
