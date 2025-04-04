from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.breed_service import BreedService
from ..utils.decorators import role_required
from backend_app.schema_dto.breed_schema_dto import BreedSchemaDTO
from marshmallow import ValidationError

class BreedList(Resource):
    role_required('client', 'admin')
    def get(self):
        """Listar todas as raças"""
        breeds, status = BreedService.list_breeds()
        return make_response(jsonify(breeds), status)

    @role_required('client', 'admin')  # Client pode cadastrar novas raças
    def post(self):
        """Cadastrar nova raça"""
        try:
            schema_dto = BreedSchemaDTO().load(request.json)
            new_breed, status = BreedService.register(schema_dto)
            return make_response(jsonify(new_breed), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code
class BreedDetail(Resource):
    
    role_required('client', 'admin')
    def get(self, id):
        """Buscar raça pelo ID"""
        breed, status = BreedService.list_breed_id(id)
        return make_response(jsonify(breed), status)

    @role_required('admin')
    def put(self, id):
        """Atualizar raça por ID"""
        breed_db, status = BreedService.list_breed_id(id)
        if status != 200:
            return make_response(jsonify(breed_db), status)
        try:
            schema_dto = BreedSchemaDTO().load(request.json)
            updated_breed, status = BreedService.update(id, schema_dto)
            return make_response(jsonify(updated_breed), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code

    @role_required('admin')
    def delete(self, id):
        """Excluir raça por ID"""
        response, status = BreedService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(BreedList, '/breeds')
api.add_resource(BreedDetail, '/breeds/<int:id>')
