from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.contact_service import ContactService
from backend_app.schema_dto.contact_schema_dto import ContactSchemaDTO
from marshmallow import ValidationError
from ..utils.decorators import role_required, contact_belongs_to_user_or_admin
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
            new_contact, status = ContactService.register(schema_dto)
            return make_response(jsonify(new_contact), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code
class ContactDetail(Resource):
    
    @contact_belongs_to_user_or_admin("id")
    def get(self, id):
        """Buscar contato pelo ID"""
        contact, status = ContactService.list_contact_id(id)
        return make_response(jsonify(contact), status)

    @contact_belongs_to_user_or_admin("id")
    def put(self, id):
        """Atualizar contato por ID"""
        contact_db, status = ContactService.list_contact_id(id)
        if status != 200:
            return make_response(jsonify(contact_db), status)

        try:
            schema_dto = ContactSchemaDTO().load(request.json)
            updated_contact, status = ContactService.update(id, schema_dto)
            return make_response(jsonify(updated_contact), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code
        
    @role_required('admin')
    def delete(self, id):
        """Excluir contato por ID"""
        response, status = ContactService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(ContactList, '/contacts')
api.add_resource(ContactDetail, '/contacts/<int:id>')
