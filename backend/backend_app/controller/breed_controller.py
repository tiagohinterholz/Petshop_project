from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.breed_service import (
    list_breeds, list_breed_id, register_breed, update_breed, delete_breed
)
from backend.backend_app.repository.breed_repository import BreedSchema
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required

class BreedList(Resource):
    @jwt_required()
    def get(self):
        """Listar todas as raças"""
        breeds, status = list_breeds()
        return make_response(jsonify(breeds), status)

    @role_required('client')  # Client pode cadastrar novas raças
    def post(self):
        """Cadastrar nova raça"""
        
        new_breed, status = register_breed(request.json)
        return make_response(jsonify(new_breed), status)

class BreedDetail(Resource):
    @jwt_required()
    def get(self, id):
        """Buscar raça pelo ID"""
        breed, status = list_breed_id(id)
        return make_response(jsonify(breed), status)

    @role_required('admin')
    def put(self, id):
        """Atualizar raça por ID"""
        breed_db, status = list_breed_id(id)
        if status != 200:
            return make_response(jsonify(breed_db), status)

        updated_breed, status = update_breed(breed_db, request.json)
        return make_response(jsonify(updated_breed), status)

    @role_required('admin')
    def delete(self, id):
        """Excluir raça por ID"""
        response, status = delete_breed(id)
        return make_response(jsonify(response), status)

api.add_resource(BreedList, '/breeds')
api.add_resource(BreedDetail, '/breeds/<int:id>')
