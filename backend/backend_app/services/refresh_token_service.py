from flask_jwt_extended import create_refresh_token, get_jwt_identity
from backend_app.schemas.refresh_token_schema import RefreshTokenSchema

def generate_refresh_token(data):
    """Gera um novo refresh token para o usuário autenticado."""
    # Validar os dados usando o RefreshTokenSchema
    validation_errors = RefreshTokenSchema().validate(data)
    if validation_errors:
        return {"error": validation_errors}, 400
    
    identity = get_jwt_identity()
    if not identity:
        return {"error": "Usuário não autenticado"}, 401
    
    refresh_token = create_refresh_token(identity=identity)
    return {"refresh_token": refresh_token}, 200