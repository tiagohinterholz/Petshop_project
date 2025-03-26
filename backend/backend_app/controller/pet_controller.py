from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.pet_service import PetService
from backend_app.schema_dto.pet_schema_dto import PetSchemaDTO
from ..utils.decorators import role_required, pet_belongs_to_user_or_admin
from marshmallow import ValidationError

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
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code 
class PetDetail(Resource):
    
    @pet_belongs_to_user_or_admin("id")
    def get(self, id):
        """Buscar pet pelo ID"""
        pet, status = PetService.list_pet_id(id)
        return make_response(jsonify(pet), status)

    @pet_belongs_to_user_or_admin("id")
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
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code 
    
    @pet_belongs_to_user_or_admin("id")
    def delete(self, id):
        """Excluir pet por ID"""
        response, status = PetService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(PetList, '/pets')
api.add_resource(PetDetail, '/pets/<int:id>')
