from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.procedure_service import ProcedureService
from ..utils.decorators import role_required, appointment_belongs_to_user_or_admin
from backend_app.schema_dto.procedure_schema_dto import ProcedureSchemaDTO
from backend_app.schema_dto.procedure_update_schema_dto import ProcedureUpdateSchemaDTO
from marshmallow import ValidationError

class ProcedureList(Resource):
    
    @role_required('admin', 'client')
    def get(self):
        """Listar todos os atendimentos"""
        procedures, status = ProcedureService.list_procedures()
        return make_response(jsonify(procedures), status)
    
    @role_required('admin')
    def post(self):
        """Cadastrar novo procedimento"""
        try:
            schema_dto = ProcedureSchemaDTO().load(request.json)
            new_procedure, status = ProcedureService.register(schema_dto)
            return make_response(jsonify(new_procedure), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code

class ProcedureDetail(Resource):
    
    @role_required('admin')
    def get(self, id):
        """Buscar procedimento pelo ID"""
        procedure, status = ProcedureService.list_procedure_id(id)        
        return make_response(jsonify(procedure), status)

    @role_required('admin')
    def put(self, id):
        """Atualizar procedimento por ID"""
        procedure_db, status = ProcedureService.list_procedure_id(id)
        if status != 200:
            return make_response(jsonify(procedure_db), status)
        
        try:
            schema_dto = ProcedureUpdateSchemaDTO().load(request.json)
            updated_appointment, status = ProcedureService.update(id, schema_dto)        
            return make_response(jsonify(updated_appointment), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code  

    @role_required('admin')
    def delete(self, id):
        """Excluir procedimento por ID""" 
        response, status = ProcedureService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(ProcedureList, '/procedures')
api.add_resource(ProcedureDetail, '/procedures/<int:id>')