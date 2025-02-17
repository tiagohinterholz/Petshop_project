from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def role_required(required_role):
    """
    Decorator para restringir o acesso com base no perfil do usuário.
    :param required_role: 'admin' ou 'client'
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Verifica se há um token válido
            claims = get_jwt()
            user_role = claims.get("profile")

            if user_role != required_role:
                return jsonify({"message": "Acesso negado. Permissão insuficiente."}), 403
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def client_owns_data(get_user_id_func):
    """
    Decorator para garantir que o cliente só acesse os próprios dados.
    :param get_user_id_func: Função que recebe *args, **kwargs e retorna o ID do usuário da requisição.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("profile")
            user_cpf = get_jwt_identity()
            
            # Obtém o CPF do usuário referente à requisição
            requested_user_id = get_user_id_func(*args, **kwargs)
            
            # Se for admin, permite acesso total
            if user_role == "admin":
                return func(*args, **kwargs)
            
            # Se for client, verifica se está acessando os próprios dados
            if user_role == "client" and str(requested_user_id) != str(user_cpf):
                return jsonify({"message": "Acesso negado. Você só pode acessar seus próprios dados."}), 403
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator