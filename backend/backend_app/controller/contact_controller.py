from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.contact_service import (
    list_contacts, list_contact_id, register_contact, update_contact, delete_contact
)
from backend.backend_app.repository.contact_repository import ContactSchema
from ..utils.decorators import role_required, client_owns_data

class ContactList(Resource):
    
    @role_required('admin')
    def get(self):
        """Listar todos os contatos"""
        contacts, status = list_contacts()
        return make_response(jsonify(contacts), status)
    
    @role_required('client')
    def post(self):
        """Cadastrar novo contato""" 
        new_contact, status = register_contact(request.json)
        return make_response(jsonify(new_contact), status)

class ContactDetail(Resource):
    
    @client_owns_data(lambda id: list_contact_id(id)[0].client_id if isinstance(list_contact_id(id)[0], dict) else None)
    def get(self, id):
        """Buscar contato pelo ID"""
        contact, status = list_contact_id(id)
        return make_response(jsonify(contact), status)

    @client_owns_data(lambda id: list_contact_id(id)[0].client_id if isinstance(list_contact_id(id)[0], dict) else None)
    def put(self, id):
        """Atualizar contato por ID"""
        contact_db, status = list_contact_id(id)
        if status != 200:
            return make_response(jsonify(contact_db), status)

        updated_contact, status = update_contact(contact_db, request.json)
        return make_response(jsonify(updated_contact), status)
    
    @role_required('admin')
    def delete(self, id):
        """Excluir contato por ID"""
        response, status = delete_contact(id)
        return make_response(jsonify(response), status)

api.add_resource(ContactList, '/contacts')
api.add_resource(ContactDetail, '/contacts/<int:id>')
