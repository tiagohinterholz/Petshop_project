from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.appointment_service import (
    list_appointments, list_appointment_id, register_appointment, update_appointment, delete_appointment
)
from backend_app.schemas.appointment_schema import AppointmentSchema
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required, client_owns_data

class AppointmentList(Resource):
    @role_required('admin')
    def get(self):
        """Listar todos os atendimentos"""
        appointments, status = list_appointments()
        return make_response(jsonify(appointments), status)

    @role_required('client')
    def post(self):
        """Cadastrar novo atendimento"""
        new_appointment, status = register_appointment(request.json)
        return make_response(jsonify(new_appointment), status)

class AppointmentDetail(Resource):
    @client_owns_data(lambda id: list_appointment_id(id)[0].get("pet_id") if isinstance(list_appointment_id(id)[0], dict) else None)
    def get(self, id):
        """Buscar atendimento pelo ID"""
        appointment, status = list_appointment_id(id)        
        return make_response(jsonify(appointment), status)

    @client_owns_data(lambda id: list_appointment_id(id)[0].get("pet_id") if isinstance(list_appointment_id(id)[0], dict) else None)
    def put(self, id):
        """Atualizar atendimento por ID"""
        appointment_db, status = list_appointment_id(id)
        if status != 200:
            return make_response(jsonify(appointment_db), status)

        updated_appointment, status = update_appointment(appointment_db, request.json)
        return make_response(jsonify(updated_appointment), status) 

    @role_required('admin')
    def delete(self, id):
        """Excluir atendimento por ID""" 
        response, status = delete_appointment(id)
        return make_response(jsonify(response), status)

api.add_resource(AppointmentList, '/appointments')
api.add_resource(AppointmentDetail, '/appointments/<int:id>')
