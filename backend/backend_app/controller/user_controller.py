from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.user_service import UserService
from backend_app.schema_dto.user_schema_dto import UserSchemaDTO
from backend_app.schema_dto.user_update_schema_dto import UserUpdateSchemaDTO
from ..utils.decorators import role_required, owner_or_admin_required 
from marshmallow import ValidationError

class UserList(Resource):
    @role_required('admin')
    def get(self):
        """Listar todos os usuários"""
        
        users, status = UserService.list_users()
        return make_response(jsonify(users), status)
    
    @role_required('admin')
    def post(self):
        """Cadastrar novo usuário"""
        try:
            schema_dto = UserSchemaDTO().load(request.json)
            new_user, status = UserService.register(schema_dto)
            return make_response(jsonify(new_user), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code
        except Exception:
            return {"error": "Erro interno do Servidor"}, 500 
class UserDetail(Resource):
    
    @owner_or_admin_required()
    def get(self, id):
        """Buscar usuário pelo CPF"""
        user, status = UserService.list_user_id(id)
        return make_response(jsonify(user), status)
    
    @owner_or_admin_required()
    def put(self, id):
        """Atualizar dados de usuário apenas por ADMIN"""
        user_db, status = UserService.list_user_id(id)
        if status != 200:
            return make_response(jsonify(user_db), status)

        try:
            schema_dto = UserUpdateSchemaDTO().load(request.json)
            updated_user, status = UserService.update(id, schema_dto)
            return make_response(jsonify(updated_user), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return make_response(jsonify({"error": err.messages}), status_code)
        
    @role_required('admin')
    def delete(self, id):
        """Excluir usuário por ID"""
        response, status = UserService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<int:id>')
