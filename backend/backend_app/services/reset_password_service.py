from backend_app.repository.user_repository import UserRepository
from backend_app.repository.password_reset_repository import PasswordResetRepository
from flask_jwt_extended import decode_token
from passlib.hash import pbkdf2_sha256

def reset_password(data):
    """Redefine a senha do usuário usando o token de recuperação"""
    
    # Debug: Dados chegando no serviço
    
    token = data.get("token")
    new_password = pbkdf2_sha256.hash(data.get('new_password'))
    
   
    # Verificar se o token está no banco
    reset_entry = PasswordResetRepository.get_by_token(token)
    
    if not reset_entry:
        return {"error": "Token inválido."}, 401
    
    if reset_entry.is_expired():
        return {"error": "Token expirado."}, 401
    
    if reset_entry.used:
        return {"error": "Token já utilizado."}, 401
    
    try:
        decoded_token = decode_token(token)
        email = decoded_token.get("sub")  # O e-mail foi salvo como identidade no JWT
    except Exception:
        return {"error": "Token inválido ou expirado."}, 401
    
    
    user = UserRepository.get_by_email(email)
    if not user:
        print(f"Usuário com email {email} não encontrado!")
        return {"error": "Usuário não encontrado."}, 404
    
    # Atualizar a senha do usuário
    UserRepository.update_password(user, new_password)

    # Marcar o token como usado
    PasswordResetRepository.mark_as_used(token)
    
    return {"message": "Senha redefinida com sucesso."}, 200
