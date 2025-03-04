from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.client_service import (
    list_clients, list_client_id, register_client, update_client, delete_client
)
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required, client_owns_data

class ClientList(Resource):

    @role_required('admin')
    def get(self):
        """Listar todos clientes"""
        clients, status = list_clients()
        return make_response(jsonify(clients), status) 
    
    @jwt_required()
    def post(self):
        """Cadastrar novo cliente"""       
        new_client, status = register_client(request.json)
        return make_response(jsonify(new_client), status)
class ClientDetail(Resource):

    @role_required('admin')
    def get(self, id):
        """Buscar cliente pelo ID"""
        client, status = list_client_id(id)
        return make_response(jsonify(client), status)

    @client_owns_data(lambda id: list_client_id(id)[0].get("cpf") if isinstance(list_client_id(id)[0], dict) else None)
    def put(self, id):
        """Atualizar cliente por ID"""
        client_db, status = list_client_id(id)
        if status != 200:
            return make_response(jsonify(client_db), status)

        updated_client, status = update_client(client_db, request.json)
        return make_response(jsonify(updated_client), status)

    @role_required('admin')
    def delete(self, id):
        """Excluir cliente por ID"""
        
        response, status = delete_client(id)
        return make_response(jsonify(response), status)

api.add_resource(ClientList, '/clients')
api.add_resource(ClientDetail, '/clients/<int:id>')
