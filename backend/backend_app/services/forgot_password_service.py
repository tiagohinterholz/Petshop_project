from backend_app.repository.user_repository import UserRepository
from backend_app.repository.password_reset_repository import PasswordResetRepository
from flask_jwt_extended import create_access_token
from datetime import timedelta

# Simulação de envio de e-mail (deve ser implementado com um serviço real de e-mail)
def send_reset_email(email, token):
    print(f"E-mail enviado para {email} com o token de redefinição: {token}")

def forgot_password(data):
    """Gera um token de recuperação de senha e armazena no banco"""
       
    email = data.get("email")
    user = UserRepository.get_by_email(email)
    
    if not user:
        return {"error": "E-mail não cadastrado."}, 404
    
    # Criar um token de reset
    reset_token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))

    # Salvar no banco
    PasswordResetRepository.create(user.cpf, reset_token)

    send_reset_email(email, reset_token)  # Simula envio de e-mail
    
    return {
    "message": "Instruções de redefinição de senha enviadas para seu e-mail.",
    "reset_token": reset_token
    }, 200
