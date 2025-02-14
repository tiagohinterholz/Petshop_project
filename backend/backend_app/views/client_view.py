from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.client_service import (
    list_clients, list_client_id, register_client, update_client, delete_client
)
from backend_app.schemas.client_schema import ClientSchema
from flask_jwt_extended import jwt_required
class ClientList(Resource):
    def get(self):
        """Listar todos clientes"""
        clients = list_clients()
        schema = ClientSchema(many=True)
        return make_response(jsonify(schema.dump(clients)), 200)
    
    @jwt_required()
    def post(self):
        """Cadastrar novo cliente"""
        schema = ClientSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        client = schema.load(request.json)
        new_client = register_client(client)
        return make_response(schema.jsonify(new_client), 201)

class ClientDetail(Resource):
    def get(self, id):
        """Buscar cliente pelo ID"""
        client = list_client_id(id)
        if not client:
            return make_response(jsonify({'error': 'Cliente não encontrada'}), 404)
        
        schema = ClientSchema()
        return make_response(jsonify(schema.dump(client)), 200)
    
    @jwt_required()
    def put(self, id):
        """Atualizar clientes por ID"""
        client_db = list_client_id(id)
        if not client_db:
            return make_response(jsonify({'error': 'Cliente não encontrada'}), 404)
        
        schema = ClientSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        new_client_data = schema.load(request.json)
        updated_client = update_client(client_db, new_client_data)
        return make_response(schema.jsonify(updated_client), 200)
    
    @jwt_required()
    def delete(self, id):
        """Excluir cliente por id"""
        client = list_client_id(id)
        if not client:
            return make_response(jsonify({'error': 'Cliente não encontrada'}), 404)
        
        delete_client(client)
        return make_response('', 204)

api.add_resource(ClientList, '/clients')
api.add_resource(ClientDetail, '/clients/<int:id>')