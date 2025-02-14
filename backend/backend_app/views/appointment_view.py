from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.appointment_service import (
    list_appointments, list_appointment_id, register_appointment, update_appointment, delete_appointment
)
from backend_app.schemas.appointment_schema import AppointmentSchema
from flask_jwt_extended import jwt_required

class AppointmentList(Resource):
    def get(self):
        """Listar todos atendimentos"""
        appointment = list_appointments()
        schema = AppointmentSchema(many=True)
        return make_response(jsonify(schema.dump(appointment)), 200)
    
    @jwt_required()
    def post(self):        
        """Cadastrar novo atendimento"""
              
        schema = AppointmentSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        appointment = schema.load(request.json)
        new_appointment = register_appointment(appointment)
        return make_response(schema.jsonify(new_appointment), 201)

class AppointmentDetail(Resource):
    def get(self, id):
        """Buscar atendimento pelo ID"""
        appointment = list_appointment_id(id)
        if not appointment:
            return make_response(jsonify({'error': 'Atendimento não encontrado'}), 404)
        
        schema = AppointmentSchema()
        return make_response(jsonify(schema.dump(appointment)), 200)
    
    @jwt_required()
    def put(self, id):
        """Atualizar atendimentos por ID"""
        appointment_db = list_appointment_id(id)
        if not appointment_db:
            return make_response(jsonify({'error': 'Atendimento não encontrado'}), 404)
        
        schema = AppointmentSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        new_appointment = schema.load(request.json)
        update_appointment = update_appointment(appointment_db, new_appointment)
        return make_response(schema.jsonify(update_appointment), 200)
    
    @jwt_required()
    def delete(self, id):
        """Excluir atendimentos por id"""
        appointment = list_appointment_id(id)
        if not appointment:
            return make_response(jsonify({'error': 'Atendimento não encontrado'}), 404)
        
        delete_appointment(appointment)
        return make_response('', 204)

api.add_resource(AppointmentList, '/appointments')
api.add_resource(AppointmentDetail, '/appointments/<int:id>')