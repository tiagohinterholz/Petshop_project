from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.contact_service import (
    list_contacts, list_contact_id, register_contact, update_contact, delete_contact
)
from backend_app.schemas.contact_schema import ContactSchema
from ..utils.decorators import role_required, client_owns_data

class ContactList(Resource):
    
    @role_required('admin')
    def get(self):
        """Listar todos os contatos"""
        contacts = list_contacts()
        schema = ContactSchema(many=True)
        return make_response(jsonify(schema.dump(contacts)), 200)
    
    @role_required('client')
    def post(self):
        """Cadastrar novo contato"""
        schema = ContactSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)

        contact = schema.load(request.json)
        new_contact, status = register_contact(contact)
        return make_response(jsonify(schema.dump(new_contact)), status)

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

        schema = ContactSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)

        new_contact = schema.load(request.json)
        updated_contact, status = update_contact(contact_db, new_contact)
        return make_response(jsonify(schema.dump(updated_contact)), status)
    
    @role_required('admin')
    def delete(self, id):
        """Excluir contato por ID"""
        contact, status = list_contact_id(id)
        if status != 200:
            return make_response(jsonify(contact), status)

        delete_contact(contact)
        return make_response(jsonify({"message": "Contato excluído com sucesso"}), 204)

api.add_resource(ContactList, '/contacts')
api.add_resource(ContactDetail, '/contacts/<int:id>')
