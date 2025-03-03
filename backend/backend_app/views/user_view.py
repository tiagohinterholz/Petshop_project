from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.user_service import (
    register_user, delete_user, list_user_id, update_user, list_users
)
from flask_jwt_extended import get_jwt_identity
from ..utils.decorators import role_required

class UserList(Resource):
    @role_required('admin')
    def get(self):
        """Listar todos os usuários"""
        users, status = list_users()
        return make_response(jsonify(users), status)

    def post(self):
        """Cadastrar novo usuário"""
        new_user, status = register_user(request.json)
        return make_response(jsonify(new_user), status)

class UserDetail(Resource):
    @role_required('admin')
    def put(self, cpf):
        """Atualizar dados de usuário apenas por ADMIN"""
        user_db, status = list_user_id(cpf)
        if status != 200:
            return make_response(jsonify(user_db), status)

        new_user_data = request.json
        updated_user, status = update_user(user_db, new_user_data)
        return make_response(jsonify(updated_user), status)

    @role_required('admin')
    def delete(self, cpf):
        """Excluir usuário por CPF"""
        response, status = delete_user(cpf)
        return make_response(jsonify(response), status)

api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<string:cpf>')
