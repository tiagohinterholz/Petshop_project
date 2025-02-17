from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.breed_service import (
    list_breeds, list_breed_id, register_breed, update_breed, delete_breed
)
from backend_app.schemas.breed_schema import BreedSchema
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required, client_owns_data

class BreedList(Resource):
    @role_required('client')
    def get(self):
        """Listar todas raças"""
        breeds = list_breeds()
        schema = BreedSchema(many=True)
        return make_response(jsonify(schema.dump(breeds)), 200)
    
    @role_required('client')
    def post(self):
        """Cadastrar nova raça"""
        schema = BreedSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        breed = schema.load(request.json)
        new_breed = register_breed(breed)
        return make_response(schema.jsonify(new_breed), 201)

class BreedDetail(Resource):
    @jwt_required()
    def get(self, id):
        """Buscar raça pelo ID"""
        breed = list_breed_id(id)
        if not breed:
            return make_response(jsonify({'error': 'Raça não encontrada'}), 404)
        
        schema = BreedSchema()
        return make_response(jsonify(schema.dump(breed)), 200)
    
    @role_required('admin')
    def put(self, id):
        """Atualizar raças por ID"""
        breed_db = list_breed_id(id)
        if not breed_db:
            return make_response(jsonify({'error': 'Raça não encontrada'}), 404)
        
        schema = BreedSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        new_breed = schema.load(request.json)
        update_breed = update_breed(breed_db, new_breed)
        return make_response(schema.jsonify(update_breed), 200)
    
    @role_required('admin')
    def delete(self, id):
        """Excluir raça por id"""
        breed = list_breed_id(id)
        if not breed:
            return make_response(jsonify({'error': 'Raça não encontrada'}), 404)
        
        delete_breed(breed)
        return make_response('', 204)

api.add_resource(BreedList, '/breeds')
api.add_resource(BreedDetail, '/breeds/<int:id>')