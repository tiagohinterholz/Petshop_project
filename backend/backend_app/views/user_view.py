from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.user_service import register_user, delete_user, list_user_id, update_user
from backend_app.schemas.user_schema import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
class UserList(Resource):   
    def post(self):        
        """Cadastrar novo user"""
              
        schema = UserSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        # bloqueio para impedir que qualquer usuário se cadastre como admin        
        if request.json.get("profile") == "ADMIN":
            return make_response(jsonify({"error": "Não é permitido criar um usuário ADMIN."}), 403)
      
        user = schema.load(request.json)
        
        new_user = register_user(user)
        return make_response(schema.jsonify(new_user), 201)

class UserDetail(Resource):
    
    @jwt_required()
    def put(self, cpf):
        """Atualiza dados de PERFIL do usuário apenas por ADMIN"""
        user_db = list_user_id(cpf)
        if not user_db:
            return make_response(jsonify({'error': 'Usuário não encontrado'}), 404)
        
        schema = UserSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        current_user = get_jwt_identity()
        logged_user = list_user_id(current_user)
        
        if 'profile' in request.json:
            if logged_user.profile != "ADMIN":
                return make_response(jsonify({"error": "Apenas administradores podem alterar perfis de usuário"}), 403)
        
        new_user = schema.load(request.json)
        updated_user = update_user(user_db, new_user)
        return make_response(schema.jsonify(updated_user), 200)
        
    @jwt_required()    
    def delete(self, cpf):
        """Excluir user por id"""
        user = list_user_id(cpf)
        if not cpf:
            return make_response(jsonify({'error': 'CPF não encontrado'}), 404)
        
        delete_user(cpf)
        return make_response('', 204)

api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<string:cpf>')