from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.contact_service import (
    list_contacts, list_contact_id, register_contact, update_contact, delete_contact
)
from backend_app.schemas.contact_schema import ContactSchema
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required, client_owns_data

class ContactList(Resource):
    
    @role_required('admin')
    def get(self):
        """Listar todos contatos"""
        contacts = list_contacts()
        schema = ContactSchema(many=True)
        return make_response(jsonify(schema.dump(contacts)), 200)
    
    @role_required('client')
    def post(self):        
        """Cadastrar novo contact"""
              
        schema = ContactSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        contact = schema.load(request.json)
        new_contact = register_contact(contact)
        return make_response(schema.jsonify(new_contact), 201)

class ContactDetail(Resource):
    
    @role_required('admin')
    def get(self, id):
        """Buscar contato pelo ID"""
        contact = list_contact_id(id)
        if not contact:
            return make_response(jsonify({'error': 'Contato não encontrado'}), 404)
        
        schema = ContactSchema()
        return make_response(jsonify(schema.dump(contact)), 200)
    
    @client_owns_data(lambda id: list_contact_id(id).user_cpf)
    def put(self, id):
        """Atualizar contato por ID"""
        contact_db = list_contact_id(id)
        if not contact_db:
            return make_response(jsonify({'error': 'Contato não encontrado'}), 404)
        
        schema = ContactSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        new_contact = schema.load(request.json)
        update_contact = update_contact(contact_db, new_contact)
        return make_response(schema.jsonify(update_contact), 200)
    
    @role_required('admin')
    def delete(self, id):
        """Excluir contato por id"""
        contact = list_contact_id(id)
        if not contact:
            return make_response(jsonify({'error': 'Contato não encontrado'}), 404)
        
        delete_contact(contact)
        return make_response('', 204)

api.add_resource(ContactList, '/contacts')
api.add_resource(ContactDetail, '/contacts/<int:id>')