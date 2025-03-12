from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.pet_service import (
    list_pets, list_pet_id, register_pet, update_pet, delete_pet
)
from backend.backend_app.repository.pet_repository import PetSchema
from ..utils.decorators import role_required, client_owns_data
from datetime import datetime

class PetList(Resource):
    
    @role_required('admin')
    def get(self):
        """Listar todos os pets"""
        pets, status = list_pets()
        return make_response(jsonify(pets), status)
    
    @role_required('client')
    def post(self):
        """Cadastrar novo pet"""
        new_pet, status = register_pet(request.json)
        return make_response(jsonify(new_pet), status)

class PetDetail(Resource):
    
    @client_owns_data(lambda id: list_pet_id(id)[0].get("client_id") if isinstance(list_pet_id(id)[0], dict) else None)
    def get(self, id):
        """Buscar pet pelo ID"""
        pet, status = list_pet_id(id)
        return make_response(jsonify(pet), status)

    @client_owns_data(lambda id: list_pet_id(id)[0].get("client_id") if isinstance(list_pet_id(id)[0], dict) else None)
    def put(self, id):
        """Atualizar pet por ID"""
        pet_db, status = list_pet_id(id)
        if status != 200:
            return make_response(jsonify(pet_db), status)

        updated_pet, status = update_pet(pet_db, request.json)
        return make_response(jsonify(updated_pet), status)
    
    @role_required('admin')
    def delete(self, id):
        """Excluir pet por ID"""
        response, status = delete_pet(id)
        return make_response(jsonify(response), status)

api.add_resource(PetList, '/pets')
api.add_resource(PetDetail, '/pets/<int:id>')
