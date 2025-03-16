from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@jwt_required(refresh=True)  # Exige um refresh token válido no header
def generate_refresh_token():
    """Gera um novo access token usando um refresh token válido."""
    identity = get_jwt_identity()  # Obtém o usuário autenticado
    new_access_token = create_access_token(identity=identity)  # Gera um novo access token

    return {"access_token": new_access_token}, 200
