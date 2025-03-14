from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.address_service import AddressService
from ..utils.decorators import role_required, client_owns_data
from flasgger import swag_from
from backend_app.schema_dto.address_schema_dto import AddressSchemaDTO
from marshmallow import ValidationError

def get_address_id(id):
    address = AddressService.list_address_id(id)
    if address and isinstance(address[0], dict):
        return address[0].get("address_id")
    return None

class AddressList(Resource):
    @swag_from("../docs/address/get.yml")
    @role_required('admin')
    def get(self):
        """Listar todos os endereços"""
        addresses, status = AddressService.list_addresses()
        return make_response(jsonify(addresses), status)

    @swag_from("../docs/address/post.yml")
    @role_required('client')
    def post(self):        
        """Cadastrar novo endereço"""
        try:
            schema_dto = AddressSchemaDTO().load(request.json)
            new_address, status = AddressService.register(schema_dto)
            return make_response(jsonify(new_address), status)
        except ValidationError as err:
            return {"error": err.messages}, 400

class AddressDetail(Resource):
    @swag_from("../docs/address/get_id.yml")
    @client_owns_data(get_address_id)
    def get(self, id):
        """Buscar endereço pelo ID"""
        address, status = AddressService.list_address_id(id)
        return make_response(jsonify(address), status)

    @swag_from("../docs/address/put.yml")
    @client_owns_data(get_address_id)
    def put(self, id):
        """Atualizar endereço por ID"""
        address_db, status = AddressService.list_address_id(id)
        if status != 200:
            return make_response(jsonify(address_db), status)
        
        try:
            schema_dto = AddressSchemaDTO().load(request.json)
            updated_address, status = AddressService.update(id, schema_dto)        
            return make_response(jsonify(updated_address), status)
        except ValidationError as err:
            return {"error": err.messages}, 400  
    
    @swag_from("../docs/address/delete.yml")
    @role_required('admin')
    def delete(self, id):
        """Excluir endereço por ID"""
        response, status = AddressService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(AddressList, '/addresses')
api.add_resource(AddressDetail, '/addresses/<int:id>')
