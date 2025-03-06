from marshmallow import ValidationError
from backend_app import db
from backend_app.models.user_model import User
from backend_app.schemas.user_schema import UserSchema

def list_users():
    """Retorna todos os usuários cadastrados."""
    try:
        users = User.query.all()
        return UserSchema(many=True).dump(users), 200
    except Exception as e:
        return {"error": f"Erro ao listar usuários: {str(e)}"}, 500

def register_user(user_data):
    """Cadastra um novo usuário."""
    schema = UserSchema()
    
    try:
        validated_data = schema.load(user_data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    
    user_db = User(
        cpf=validated_data.cpf, 
        name=validated_data.name, 
        profile=validated_data.profile.value.upper(), 
        password=validated_data.password
    )
    user_db.encrypt_password()
    
    try:
        db.session.add(user_db)
        db.session.commit()
        return schema.dump(user_db), 201  # Retorna os dados sem a senha
    except Exception as e:
        db.session.rollback()  # Evita inconsistências no banco
        return {"error": f"Erro ao cadastrar usuário: {str(e)}"}, 500

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
    if "password" in new_user_data:
        user_db.password = new_user_data["password"]
        user_db.encrypt_password() # Já deve estar encriptada no schema
        
    db.session.commit()
    return UserSchema().dump(user_db), 200 

def delete_user(cpf):
    """Exclui um usuário pelo CPF."""
    try:
        user = db.session.get(User, cpf)
        if not user:
            return {"error": "Usuário inexistente."}, 404
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "Usuário deletado com sucesso"}, 200  # Agora retorna um JSON
    except Exception as e:
        db.session.rollback()
        return {"error": f"Erro ao excluir usuário: {str(e)}"}, 500
