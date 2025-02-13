from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.address_service import (
    list_addresses, list_address_id, register_address, update_address, delete_address
)
from backend_app.schemas.address_schema import AddressSchema

class AddressList(Resource):
    def get(self):
        """Listar todos endereços"""
        addresses = list_addresses()
        schema = AddressSchema(many=True)
        return make_response(jsonify(schema.dump(addresses)), 200)
    
    def post(self):        
        """Cadastrar novo endereço"""
              
        schema = AddressSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        address = schema.load(request.json)
        new_address = register_address(address)
        return make_response(schema.jsonify(new_address), 201)

class AddressDetail(Resource):
    def get(self, id):
        """Buscar endereço pelo ID"""
        address = list_address_id(id)
        if not address:
            return make_response(jsonify({'error': 'Endereço não encontrada'}), 404)
        
        schema = AddressSchema()
        return make_response(jsonify(schema.dump(address)), 200)
    
    def put(self, id):
        """Atualizar endereços por ID"""
        address_db = list_address_id(id)
        if not address_db:
            return make_response(jsonify({'error': 'Endereço não encontrada'}), 404)
        
        schema = AddressSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        new_address = schema.load(request.json)
        update_address = update_address(address_db, new_address)
        return make_response(schema.jsonify(update_address), 200)
    
    def delete(self, id):
        """Excluir endereço por id"""
        address = list_address_id(id)
        if not address:
            return make_response(jsonify({'error': 'Endereço não encontrado'}), 404)
        
        delete_address(address)
        return make_response('', 204)

api.add_resource(AddressList, '/address')
api.add_resource(AddressDetail, '/address/<int:id>')