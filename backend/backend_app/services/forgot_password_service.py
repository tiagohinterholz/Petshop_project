import secrets
from backend_app.models.user_model import User
from backend_app import db
from backend.backend_app.schema_dto.forgot_password_schema_dto import ForgotPasswordSchema
from flask_jwt_extended import create_access_token
from datetime import timedelta

# Simulação de envio de e-mail (deve ser implementado com um serviço real de e-mail)
def send_reset_email(email, token):
    print(f"E-mail enviado para {email} com o token de redefinição: {token}")

def forgot_password(data):
    """Gera um JWT de recuperação de senha e envia por e-mail."""
    # Validar entrada com o schema
    validation_errors = ForgotPasswordSchema().validate(data)
    if validation_errors:
        return {"error": validation_errors}, 400
    
    email = data.get("email")
    user = db.session.query(User).filter_by(email=email).first()
    
    if not user:
        return {"error": "E-mail não cadastrado."}, 404
    
    # Gerar um JWT como token de recuperação (expira em 15 minutos)
    reset_token = create_access_token(identity=email, expires_delta=timedelta(minutes=5))
    
    send_reset_email(email, reset_token)  # Simula envio de e-mail
    
    return {"message": "Instruções de redefinição de senha enviadas para seu e-mail."}, 200
