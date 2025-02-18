from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.breed_service import (
    list_breeds, list_breed_id, register_breed, update_breed, delete_breed
)
from backend_app.schemas.breed_schema import BreedSchema
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required

class BreedList(Resource):
    @jwt_required()
    def get(self):
        """Listar todas as raças"""
        breeds = list_breeds()
        schema = BreedSchema(many=True)
        return make_response(jsonify(schema.dump(breeds)), 200)

    @role_required('client')  # Client pode cadastrar novas raças
    def post(self):
        """Cadastrar nova raça"""
        schema = BreedSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        breed = schema.load(request.json)
        new_breed, status = register_breed(breed)

        if isinstance(new_breed, dict) and "error" in new_breed:
            return make_response(jsonify(new_breed), status)

        return make_response(jsonify(schema.dump(new_breed)), 201)

class BreedDetail(Resource):
    @jwt_required()
    def get(self, id):
        """Buscar raça pelo ID"""
        breed, status = list_breed_id(id)
        if status != 200:
            return make_response(jsonify(breed), status)

        schema = BreedSchema()
        return make_response(jsonify(schema.dump(breed)), 200)

    @role_required('admin')
    def put(self, id):
        """Atualizar raça por ID"""
        breed_db, status = list_breed_id(id)
        if status != 200:
            return make_response(jsonify(breed_db), status)

        schema = BreedSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        new_breed = schema.load(request.json)
        updated_breed, status = update_breed(breed_db, new_breed)
        return make_response(jsonify(schema.dump(updated_breed)), status)

    @role_required('admin')
    def delete(self, id):
        """Excluir raça por ID"""
        breed, status = list_breed_id(id)
        if status != 200:
            return make_response(jsonify(breed), status)

        delete_message, status = delete_breed(breed)
        return make_response(jsonify(delete_message), status)

api.add_resource(BreedList, '/breeds')
api.add_resource(BreedDetail, '/breeds/<int:id>')
