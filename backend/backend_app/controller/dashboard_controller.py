from flask import request, jsonify, make_response
from flask_restful import Resource
from ..utils.decorators import owner_or_admin_required
from backend_app.services.client_service import ClientService
from backend_app.services.address_service import AddressService 
from backend_app.services.contact_service import ContactService 
from backend_app.services.pet_service import PetService 
from backend_app.services.appointment_service import AppointmentService
from backend_app import api

class Dashboard(Resource):
    
    @owner_or_admin_required()
    def get(self, id):
        
        client, status = ClientService.list_client_user_id(id) 
        if status != 200:
            return make_response(jsonify(client), status)
        
        if not client or "id" not in client:
            return make_response(jsonify({
            "client": [],
            "address": [],
            "contact": [],
            "pets": []
        }), 200)
        
        client_id = client["id"]
        address, status = AddressService.list_address_client_id(client_id)
        contact, status = ContactService.list_contact_client_id(client_id)
        pets, status = PetService.list_pet_client_id(client_id)
        
        pets_with_appointments = []
        
        for pet in pets:
            pet_id = pet["id"]
            appointments, _ = AppointmentService.list_appointment_pet_id(pet_id)
            pet["appointments"] = appointments
            pets_with_appointments.append(pet)
        
        return make_response(jsonify({
            "client": client,
            "address": address,
            "contact": contact,
            "pets": pets_with_appointments
        }), 200)
        
api.add_resource(Dashboard, '/dashboard/<int:id>')    