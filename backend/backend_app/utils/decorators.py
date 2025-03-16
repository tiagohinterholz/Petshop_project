from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity

def role_required(*required_role):
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

            if not user_role:
                return {"message": "Token inválido ou ausente."}, 401

            if user_role not in required_role:
                return {
                    "message": f"Acesso negado. Permissão insuficiente. Requer: {required_role}, Seu perfil: {user_role}"
                }, 403
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def client_owns_data(get_client_id_func):
    """
    Decorator para garantir que o cliente só acesse os próprios dados.
    :param get_user_id_func: Função que recebe *args, **kwargs e retorna o id do client da requisição.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("profile")
            user_cpf = get_jwt_identity()
            
            # Obtém o CPF do usuário referente à requisição
            requested_client_id = get_client_id_func(**kwargs)  # Obtém ID do cliente a partir da requisição
            
            if requested_client_id is None:
                return {"message": "Recurso não encontrado."}, 404
            
            # Se for admin, permite acesso total
            if user_role == "admin":
                return func(*args, **kwargs)

            # Se for client, verifica se está acessando os próprios dados
            if user_role == "client":
                from backend_app.repository.client_repository import ClientRepository  # Import dinâmico para evitar import circular
                user_client = ClientRepository.get_client_by_cpf(user_cpf)
            
                if not user_client or user_client.id != requested_client_id:
                    return {"message": "Acesso negado. Você só pode acessar seus próprios dados."}, 403
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator
