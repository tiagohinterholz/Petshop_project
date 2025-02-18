from backend_app import db
from backend_app.models.user_model import User
from backend_app.schemas.user_schema import UserSchema

def list_users():
    """Retorna todos os usuários cadastrados."""
    users = User.query.all()
    return UserSchema(many=True).dump(users), 200

def register_user(user_data):
    """Cadastra um novo usuário."""
    if "password" not in user_data:
        return {"error": "O campo 'password' é obrigatório."}, 400

    existing_user = db.session.get(User, user_data["cpf"])
    if existing_user:
        return {"error": "Usuário já cadastrado com esse CPF."}, 400
    
    user_db = User(
        cpf=user_data["cpf"], 
        name=user_data["name"], 
        profile=user_data["profile"].upper(), 
        password=user_data["password"]
    )
    user_db.encrypt_password()
    db.session.add(user_db)
    db.session.commit()
    
    return UserSchema().dump(user_db), 201

def list_user_id(cpf):
    """Busca usuário pelo CPF."""
    user = db.session.get(User, cpf)  
    if not user:
        return {"error": "Usuário não encontrado"}, 404
    return UserSchema().dump(user), 200  

def update_user(user_db, new_user_data):
    """Atualiza um usuário."""
    if not user_db:
        return {"error": "Usuário não encontrado"}, 404  
    
    user_db.name = new_user_data["name"]
    user_db.password = new_user_data["password"]  # Já deve estar encriptada no schema
    db.session.commit()

    return UserSchema().dump(user_db), 200 

def delete_user(cpf):
    """Exclui um usuário pelo CPF."""
    user = db.session.get(User, cpf)
    if not user:
        return {"error": "Usuário inexistente."}, 404
    
    db.session.delete(user)
    db.session.commit()
    
    return {"message": "Usuário deletado com sucesso"}, 204 
