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
        appointments = list_appointments()
        schema = AppointmentSchema(many=True)
        return make_response(jsonify(schema.dump(appointments)), 200)

    @role_required('client')
    def post(self):
        """Cadastrar novo atendimento"""
        schema = AppointmentSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)

        appointment_data = schema.load(request.json)
        new_appointment, status = register_appointment(appointment_data)
        return make_response(jsonify(schema.dump(new_appointment)), status)

class AppointmentDetail(Resource):
    @client_owns_data(lambda id: list_appointment_id(id)[0].get("pet_id") if isinstance(list_appointment_id(id)[0], dict) else None)
    def get(self, id):
        """Buscar atendimento pelo ID"""
        appointment, status = list_appointment_id(id)
        if status != 200:
            return make_response(jsonify(appointment), status)

        schema = AppointmentSchema()
        return make_response(jsonify(schema.dump(appointment)), status)

    @client_owns_data(lambda id: list_appointment_id(id)[0].get("pet_id") if isinstance(list_appointment_id(id)[0], dict) else None)
    def put(self, id):
        """Atualizar atendimento por ID"""
        appointment_db, status = list_appointment_id(id)
        if status != 200:
            return make_response(jsonify(appointment_db), status)

        schema = AppointmentSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)

        new_appointment_data = schema.load(request.json)
        updated_appointment, status = update_appointment(appointment_db, new_appointment_data)
        return make_response(jsonify(schema.dump(updated_appointment)), status) 

    @role_required('admin')
    def delete(self, id):
        """Excluir atendimento por ID"""
        appointment, status = list_appointment_id(id)
        if status != 200:
            return make_response(jsonify(appointment), status)

        message, status = delete_appointment(appointment)
        return make_response(jsonify(message), status)

api.add_resource(AppointmentList, '/appointments')
api.add_resource(AppointmentDetail, '/appointments/<int:id>')
