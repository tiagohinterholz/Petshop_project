from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.pet_service import (
    list_pets, list_pet_id, register_pet, update_pet, delete_pet
)
from backend_app.schemas.pet_schema import PetSchema
from ..utils.decorators import role_required, client_owns_data
from datetime import datetime

class PetList(Resource):
    
    @role_required('admin')
    def get(self):
        """Listar todos os pets"""
        pets = list_pets()
        schema = PetSchema(many=True)
        return make_response(jsonify(schema.dump(pets)), 200)
    
    @role_required('client')
    def post(self):
        """Cadastrar novo pet"""
        schema = PetSchema()
        data = request.json
        
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)

        pet = schema.load(request.json)
        new_pet, status = register_pet(pet)
        return make_response(jsonify(schema.dump(new_pet)), status)

class PetDetail(Resource):
    
    @client_owns_data(lambda id: list_pet_id(id)[0].client_id if isinstance(list_pet_id(id)[0], dict) else None)
    def get(self, id):
        """Buscar pet pelo ID"""
        pet, status = list_pet_id(id)
        return make_response(jsonify(pet), status)

    @client_owns_data(lambda id: list_pet_id(id)[0].client_id if isinstance(list_pet_id(id)[0], dict) else None)
    def put(self, id):
        """Atualizar pet por ID"""
        pet_db, status = list_pet_id(id)
        if status != 200:
            return make_response(jsonify(pet_db), status)

        schema = PetSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)

        new_pet = schema.load(request.json)
        updated_pet, status = update_pet(pet_db, new_pet)
        return make_response(jsonify(schema.dump(updated_pet)), status)
    
    @role_required('admin')
    def delete(self, id):
        """Excluir pet por ID"""
        pet, status = list_pet_id(id)
        if status != 200:
            return make_response(jsonify(pet), status)

        delete_pet(pet)
        return make_response(jsonify({"message": "Pet excluído com sucesso"}), 200)

api.add_resource(PetList, '/pets')
api.add_resource(PetDetail, '/pets/<int:id>')
