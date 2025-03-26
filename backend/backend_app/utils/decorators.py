from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from backend_app.models.address_model import Address
from backend_app.models.pet_model import Pet
from backend_app.models.appointment_model import Appointment
from backend_app.models.contact_model import Contact
from backend_app.models.client_model import Client

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
            user_id = get_jwt_identity()
            
            # Obtém o ID do usuário referente à requisição
            requested_client_id = get_client_id_func(**kwargs)  # Obtém ID do cliente a partir da requisição
            
            if requested_client_id is None:
                return {"message": "Recurso não encontrado."}, 404
            
            # Se for admin, permite acesso total
            if user_role == "admin":
                return func(*args, **kwargs)

            # Se for client, verifica se está acessando os próprios dados
            if user_role == "client":
                from backend_app.repository.client_repository import ClientRepository  # Import dinâmico para evitar import circular
                user_client = ClientRepository.get_client_by_cpf(user_id)
            
                if not user_client or user_client.id != requested_client_id:
                    return {"message": "Acesso negado. Você só pode acessar seus próprios dados."}, 403
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def owner_or_admin_required(param_user_id_name="id"):
    """
    Decorator que permite acesso se o user_id do token for igual ao do recurso
    OU se o usuário for admin.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            jwt_user_id = int(get_jwt_identity())  # ID vindo do token
            claims = get_jwt()
            profile = claims.get("profile")

            resource_user_id = int(kwargs.get(param_user_id_name))  # user_id da rota

            if profile == "admin" or jwt_user_id == resource_user_id:
                return func(*args, **kwargs)

            return {"message": "Acesso negado. Não pertence ao usuário logado."}, 403

        return wrapper
    return decorator

def pet_belongs_to_user_or_admin(param_pet_id="id"):
    """
    Permite acesso se o pet pertencer ao usuário logado ou se for admin.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            profile = claims.get("profile")
            user_id = int(get_jwt_identity())

            pet_id = int(kwargs.get(param_pet_id))
            pet = Pet.query.get(pet_id)

            if not pet:
                return {"message": "Pet não encontrado."}, 404

            if profile == "admin" or pet.client.user_id == user_id:
                return func(*args, **kwargs)

            return {"message": "Acesso negado. Pet não pertence a você."}, 403

        return wrapper
    return decorator

def appointment_belongs_to_user_or_admin(param_appointment_id="id"):
    """
    Permite acesso se o agendamento for do usuário logado ou se for admin.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            profile = claims.get("profile")
            user_id = int(get_jwt_identity())

            appointment_id = int(kwargs.get(param_appointment_id))
            appointment = Appointment.query.get(appointment_id)

            if not appointment:
                return {"message": "Agendamento não encontrado."}, 404

            # Aqui faz o caminho completo até o user_id do dono
            if profile == "admin" or appointment.pet.client.user_id == user_id:
                return func(*args, **kwargs)

            return {"message": "Acesso negado. Agendamento não pertence a você."}, 403

        return wrapper
    return decorator

def address_belongs_to_user_or_admin(param_address_id="id"):
    """
    Permite acesso se o endereço pertencer ao usuário logado ou se for admin.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            profile = claims.get("profile")
            user_id = int(get_jwt_identity())

            address_id = int(kwargs.get(param_address_id))
            address = Address.query.get(address_id)

            if not address:
                return {"message": "Pet não encontrado."}, 404

            if profile == "admin" or address.client.user_id == user_id:
                return func(*args, **kwargs)

            return {"message": "Acesso negado. Endereço não pertence a você."}, 403

        return wrapper
    return decorator

def contact_belongs_to_user_or_admin(param_contact_id="id"):
    """
    Permite acesso se o contato pertencer ao usuário logado ou se for admin.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            profile = claims.get("profile")
            user_id = int(get_jwt_identity())

            contact_id = int(kwargs.get(param_contact_id))
            contact = Contact.query.get(contact_id)

            if not contact:
                return {"message": "Contato não encontrado."}, 404

            if profile == "admin" or contact.client.user_id == user_id:
                return func(*args, **kwargs)

            return {"message": "Acesso negado. Contato não pertence a você."}, 403

        return wrapper
    return decorator

def client_belongs_to_user_or_admin(param_client_id="id"):
    """
    Permite acesso se o endereço pertencer ao usuário logado ou se for admin.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            profile = claims.get("profile")
            user_id = int(get_jwt_identity())

            client_id = int(kwargs.get(param_client_id))
            client = Client.query.get(client_id)

            if not client:
                return {"message": "Cliente não encontrado."}, 404

            if profile == "admin" or client.user_id == user_id:
                return func(*args, **kwargs)

            return {"message": "Acesso negado. Você não é o cliente pesquisado."}, 403

        return wrapper
    return decorator