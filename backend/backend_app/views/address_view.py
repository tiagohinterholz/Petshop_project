from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.address_service import (
    list_addresses, list_address_id, register_address, update_address, delete_address
)
from backend_app.schemas.address_schema import AddressSchema
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required, client_owns_data

class AddressList(Resource):
    @role_required('admin')
    def get(self):
        """Listar todos os endereços"""
        addresses = list_addresses()
        schema = AddressSchema(many=True)
        return make_response(jsonify(schema.dump(addresses)), 200)

    @role_required('client')
    def post(self):        
        """Cadastrar novo endereço"""
        schema = AddressSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        address = schema.load(request.json)
        new_address, status = register_address(address)  # Garantir que retorna um status válido
        
        if isinstance(new_address, dict) and "error" in new_address:
            return make_response(jsonify(new_address), status)  # Erro no serviço
        
        return make_response(jsonify(schema.dump(new_address)), 201)

class AddressDetail(Resource):
    @client_owns_data(lambda id: list_address_id(id)[0].client_id if isinstance(list_address_id(id), tuple) else None)
    def get(self, id):
        """Buscar endereço pelo ID"""
        address, status = list_address_id(id)
        if status != 200:
            return make_response(jsonify(address), status)

        schema = AddressSchema()
        return make_response(jsonify(schema.dump(address)), 200)

    @client_owns_data(lambda id: list_address_id(id)[0].client_id if isinstance(list_address_id(id), tuple) else None)
    def put(self, id):
        """Atualizar endereço por ID"""
        address_db, status = list_address_id(id)
        if status != 200:
            return make_response(jsonify(address_db), status)

        schema = AddressSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        new_address = schema.load(request.json)
        updated_address, status = update_address(address_db, new_address)
        return make_response(jsonify(schema.dump(updated_address)), status)

    @role_required('admin')
    def delete(self, id):
        """Excluir endereço por ID"""
        address, status = list_address_id(id)
        if status != 200:
            return make_response(jsonify(address), status)

        delete_message, status = delete_address(address)
        return make_response(jsonify(delete_message), status)

api.add_resource(AddressList, '/addresses')
api.add_resource(AddressDetail, '/addresses/<int:id>')
