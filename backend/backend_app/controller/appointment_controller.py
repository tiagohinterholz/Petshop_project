from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.appointment_service import AppointmentService
from ..utils.decorators import role_required, client_owns_data
from backend_app.schema_dto.appointment_schema_dto import AppointmentSchemaDTO
from marshmallow import ValidationError
from flasgger import swag_from
    
def get_appointment_pet_id(id):
    appointment = AppointmentService.list_appointment_id(id)
    if appointment and isinstance(appointment[0], dict):
        return appointment[0].get("pet_id")
    return None

class AppointmentList(Resource):
    @role_required('admin')
    def get(self):
        """Listar todos os atendimentos"""
        appointments, status = AppointmentService.list_appointments()
        return make_response(jsonify(appointments), status)

    @role_required('client')
    def post(self):
        """Cadastrar novo atendimento"""
        try:
            schema_dto = AppointmentSchemaDTO().load(request.json)
            new_appointment, status = AppointmentService.register(schema_dto)
            return make_response(jsonify(new_appointment), status)
        except ValidationError as err:
            return {"error": err.messages}, 400    

class AppointmentDetail(Resource):
    
    @client_owns_data(get_appointment_pet_id)
    def get(self, id):
        """Buscar atendimento pelo ID"""
        appointment, status = AppointmentService.list_appointment_id(id)        
        return make_response(jsonify(appointment), status)

    @client_owns_data(get_appointment_pet_id)
    def put(self, id):
        """Atualizar atendimento por ID"""
        appointment_db, status = AppointmentService.list_appointment_id(id)
        if status != 200:
            return make_response(jsonify(appointment_db), status)
        
        try:
            schema_dto = AppointmentSchemaDTO().load(request.json)
            updated_appointment, status = AppointmentService.update(id, schema_dto)        
            return make_response(jsonify(updated_appointment), status)
        except ValidationError as err:
            return {"error": err.messages}, 400  

    @client_owns_data(get_appointment_pet_id)
    def delete(self, id):
        """Excluir atendimento por ID""" 
        response, status = AppointmentService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(AppointmentList, '/appointments')
api.add_resource(AppointmentDetail, '/appointments/<int:id>')
