from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.contact_service import ContactService
from backend_app.schema_dto.contact_schema_dto import ContactSchemaDTO
from marshmallow import ValidationError
from ..utils.decorators import role_required, client_owns_data
from flasgger import swag_from

def get_contact_id(id):
    contact = ContactService.list_contact_id(id)
    if contact and isinstance(contact[0], dict):
        return contact[0].get("contact_id")
    return None 
class ContactList(Resource):
    
    @role_required('admin')
    def get(self):
        """Listar todos os contatos"""
        contacts, status = ContactService.list_contacts()
        return make_response(jsonify(contacts), status)
    
    @role_required('client')
    def post(self):
        """Cadastrar novo contato"""
        try:
            schema_dto = ContactSchemaDTO().load(request.json) 
            new_contact, status = ContactService.register_contact(schema_dto)
            return make_response(jsonify(new_contact), status)
        except ValidationError as err:
            return {"error": err.messages}, 400
class ContactDetail(Resource):
    
    @client_owns_data(get_contact_id)
    def get(self, id):
        """Buscar contato pelo ID"""
        contact, status = ContactService.list_contact_id(id)
        return make_response(jsonify(contact), status)

    @client_owns_data(get_contact_id)
    def put(self, id):
        """Atualizar contato por ID"""
        contact_db, status = ContactService.list_contact_id(id)
        if status != 200:
            return make_response(jsonify(contact_db), status)

        try:
            schema_dto = ContactSchemaDTO().load(request.json)
            updated_contact, status = ContactService.update_contact(contact_db, schema_dto)
            return make_response(jsonify(updated_contact), status)
        except ValidationError as err:
            return {"error": err.messages}, 400
        
    @role_required('admin')
    def delete(self, id):
        """Excluir contato por ID"""
        response, status = ContactService.delete_contact(id)
        return make_response(jsonify(response), status)

api.add_resource(ContactList, '/contacts')
api.add_resource(ContactDetail, '/contacts/<int:id>')
