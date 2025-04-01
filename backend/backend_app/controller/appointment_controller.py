from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.appointment_service import AppointmentService
from ..utils.decorators import role_required, appointment_belongs_to_user_or_admin
from backend_app.schema_dto.appointment_schema_dto import AppointmentSchemaDTO
from backend_app.schema_dto.appointment_update_schema_dto import AppointmentUpdateSchemaDTO
from marshmallow import ValidationError

class AppointmentList(Resource):
    @role_required('admin')
    def get(self):
        """Listar todos os atendimentos"""
        appointments, status = AppointmentService.list_appointments()
        return make_response(jsonify(appointments), status)

    @role_required('client', 'admin')
    def post(self):
        """Cadastrar novo atendimento"""
        try:
            schema_dto = AppointmentSchemaDTO().load(request.json)
            new_appointment, status = AppointmentService.register(schema_dto)
            return make_response(jsonify(new_appointment), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code   
class AppointmentDetail(Resource):
    
    @appointment_belongs_to_user_or_admin("id")
    def get(self, id):
        """Buscar atendimento pelo ID"""
        appointment, status = AppointmentService.list_appointment_id(id)        
        return make_response(jsonify(appointment), status)

    @appointment_belongs_to_user_or_admin("id")
    def put(self, id):
        """Atualizar atendimento por ID"""
        appointment_db, status = AppointmentService.list_appointment_id(id)
        if status != 200:
            return make_response(jsonify(appointment_db), status)
        
        try:
            schema_dto = AppointmentUpdateSchemaDTO().load(request.json)
            updated_appointment, status = AppointmentService.update(id, schema_dto)        
            return make_response(jsonify(updated_appointment), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code  

    @appointment_belongs_to_user_or_admin("id")
    def delete(self, id):
        """Excluir atendimento por ID""" 
        response, status = AppointmentService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(AppointmentList, '/appointments')
api.add_resource(AppointmentDetail, '/appointments/<int:id>')
