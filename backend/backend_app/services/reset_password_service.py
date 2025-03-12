from backend_app.models.user_model import User
from backend_app import db
from backend.backend_app.schema_dto.reset_password_schema_dto import ResetPasswordSchema
from flask_jwt_extended import decode_token
from passlib.hash import pbkdf2_sha256

def reset_password(data):
    """Redefine a senha do usuário usando o token de recuperação."""
    # Validar entrada com o schema
    validation_errors = ResetPasswordSchema().validate(data)
    if validation_errors:
        return {"error": validation_errors}, 400
    
    token = data.get("token")
    new_password = data.get("new_password")
    
    try:
        decoded_token = decode_token(token)  # Decodifica o JWT
        email = decoded_token.get("sub")  # O e-mail foi salvo como identidade no JWT
    except Exception:
        return {"error": "Token inválido ou expirado."}, 400
    
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return {"error": "Usuário não encontrado."}, 404
    
    # Atualizar a senha do usuário
    user.password = pbkdf2_sha256.hash(new_password)
    db.session.commit()
    
    return {"message": "Senha redefinida com sucesso."}, 200
