from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.pet_service import PetService
from backend_app.schema_dto.pet_schema_dto import PetSchemaDTO
from ..utils.decorators import role_required, client_owns_data
from marshmallow import ValidationError

def get_pet_id(id):
    pet = PetService.list_pet_id(id)
    if pet and isinstance(pet[0], dict):
        return pet[0].get("client_id")
    return None
class PetList(Resource):
    
    @role_required('admin')
    def get(self):
        """Listar todos os pets"""
        pets, status = PetService.list_pets()
        return make_response(jsonify(pets), status)
    
    @role_required('client')
    def post(self):
        """Cadastrar novo pet"""
        try:
            schema_dto = PetSchemaDTO().load(request.json)
            new_pet, status = PetService.register(schema_dto)
            return make_response(jsonify(new_pet), status)
        except ValidationError as err:
            return {"error": err.messages}, 400 
class PetDetail(Resource):
    
    @client_owns_data(get_pet_id)
    def get(self, id):
        """Buscar pet pelo ID"""
        pet, status = PetService.list_pet_id(id)
        return make_response(jsonify(pet), status)

    @client_owns_data(get_pet_id)
    def put(self, id):
        """Atualizar pet por ID"""
        pet_db, status = PetService.list_pet_id(id)
        if status != 200:
            return make_response(jsonify(pet_db), status)

        try:
            schema_dto = PetSchemaDTO().load(request.json)
            updated_pet, status = PetService.update(id, schema_dto)
            return make_response(jsonify(updated_pet), status)
        except ValidationError as err:
            return {"error": err.messages}, 400 
    
    @client_owns_data(get_pet_id)
    def delete(self, id):
        """Excluir pet por ID"""
        response, status = PetService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(PetList, '/pets')
api.add_resource(PetDetail, '/pets/<int:id>')
