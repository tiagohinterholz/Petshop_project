from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.user_service import UserService
from backend_app.schema_dto.user_schema_dto import UserSchemaDTO
from ..utils.decorators import role_required
from marshmallow import ValidationError
from flasgger import swag_from

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
            return {"error": err.messages}, 400
        except Exception as e:
            return {"error": "Erro inesperado ao cadastrar usuário", "details": str(e)}, 500 
class UserDetail(Resource):
    
    @role_required('admin')
    def get(self, cpf):
        """Buscar usuário pelo CPF"""
        user, status = UserService.list_user_id(cpf)
        return make_response(jsonify(user), status)
    
    @role_required('admin')
    def put(self, cpf):
        """Atualizar dados de usuário apenas por ADMIN"""
        user_db, status = UserService.list_user_id(cpf)
        if status != 200:
            return make_response(jsonify(user_db), status)

        try:
            schema_dto = UserSchemaDTO().load(request.json)
            updated_user, status = UserService.update(cpf, schema_dto)
            return make_response(jsonify(updated_user), status)
        except ValidationError as err:
            return {"error": err.messages}, 400

    @role_required('admin')
    def delete(self, cpf):
        """Excluir usuário por CPF"""
        response, status = UserService.delete(cpf)
        return make_response(jsonify(response), status)

api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<string:cpf>')
