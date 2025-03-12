from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.address_service import (
    list_addresses, list_address_id, register_address, update_address, delete_address
)
from ..utils.decorators import role_required, client_owns_data
from flasgger import swag_from
class AddressList(Resource):
    @swag_from("../docs/address/get.yml")
    @role_required('admin')
    def get(self):
        """Listar todos os endereços"""
        addresses, status = list_addresses()
        return make_response(jsonify(addresses), status)

    @swag_from("../docs/address/post.yml")
    @role_required('client')
    def post(self):        
        """Cadastrar novo endereço"""
        new_address, status = register_address(request.json)  # Garantir que retorna um status válido    
        return make_response(jsonify(new_address), status)

class AddressDetail(Resource):
    @swag_from("../docs/address/get_id.yml")
    @client_owns_data(lambda id: list_address_id(id)[0].get("client_id") if isinstance(list_address_id(id)[0], dict) else None)
    def get(self, id):
        """Buscar endereço pelo ID"""
        address, status = list_address_id(id)
        return make_response(jsonify(address), status)

    @swag_from("../docs/address/put.yml")
    @client_owns_data(lambda id: list_address_id(id)[0].get("client_id") if isinstance(list_address_id(id)[0], dict) else None)
    def put(self, id):
        """Atualizar endereço por ID"""
        address_db, status = list_address_id(id)
        if status != 200:
            return make_response(jsonify(address_db), status)
        
        updated_address, status = update_address(address_db, request.json)
        return make_response(jsonify(updated_address), status)
    
    @swag_from("../docs/address/delete.yml")
    @role_required('admin')
    def delete(self, id):
        """Excluir endereço por ID"""
        response, status = delete_address(id)
        return make_response(jsonify(response), status)

api.add_resource(AddressList, '/addresses')
api.add_resource(AddressDetail, '/addresses/<int:id>')
