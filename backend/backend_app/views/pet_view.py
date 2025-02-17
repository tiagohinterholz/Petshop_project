from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.pet_service import (
    list_pets, list_pet_id, register_pet, update_pet, delete_pet
)
from backend_app.schemas.pet_schema import PetSchema
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required, client_owns_data

class PetList(Resource):
    
    @role_required('admin')
    def get(self):
        """Listar todos pets"""
        pets = list_pets()
        schema = PetSchema(many=True)
        return make_response(jsonify(schema.dump(pets)), 200)
    
    @client_owns_data(lambda id: list_pet_id(id).user_cpf)
    def post(self):        
        """Cadastrar novo pet"""
              
        schema = PetSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        pet = schema.load(request.json)
        new_pet = register_pet(pet)
        return make_response(schema.jsonify(new_pet), 201)

class PetDetail(Resource):
    
    @role_required('client')
    def get(self, id):
        """Buscar raça pelo ID"""
        pet = list_pet_id(id)
        if not pet:
            return make_response(jsonify({'error': 'Raça não encontrada'}), 404)
        
        schema = PetSchema()
        return make_response(jsonify(schema.dump(pet)), 200)
    
    @role_required('admin')
    def put(self, id):
        """Atualizar raças por ID"""
        pet_db = list_pet_id(id)
        if not pet_db:
            return make_response(jsonify({'error': 'Raça não encontrada'}), 404)
        
        schema = PetSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        new_pet = schema.load(request.json)
        update_pet = update_pet(pet_db, new_pet)
        return make_response(schema.jsonify(update_pet), 200)
    
    @role_required('admin')
    def delete(self, id):
        """Excluir raça por id"""
        pet = list_pet_id(id)
        if not pet:
            return make_response(jsonify({'error': 'Raça não encontrada'}), 404)
        
        delete_pet(pet)
        return make_response('', 204)

api.add_resource(PetList, '/pets')
api.add_resource(PetDetail, '/pets/<int:id>')