from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.client_service import ClientService
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required, client_owns_data
from backend_app.schema_dto.client_schema_dto import ClientSchemaDTO

def get_client_cpf(id, **kwargs):
    client = ClientService.list_client_id(id)
    if client and isinstance(client[0], dict):
        return client[0].get("id")
    return None
class ClientList(Resource):

    @role_required('admin')
    def get(self):
        """Listar todos clientes"""
        clients, status = ClientService.list_clients()
        return make_response(jsonify(clients), status) 
    
    @jwt_required() # todos autenticados podem cadastrar novo cliente 
    def post(self):        
        """Cadastrar novo cliente"""       
        try:
            schema_dto = ClientSchemaDTO().load(request.json)
            new_client, status = ClientService.register(schema_dto)
            return make_response(jsonify(new_client), status)
        except ValidationError as err:
            status_code = 400 if "missing" in str(err.messages).lower() else 422
            return {"error": err.messages}, status_code   
class ClientDetail(Resource):

    @client_owns_data(get_client_cpf)
    def get(self, id):
        """Buscar cliente pelo ID"""
        client, status = ClientService.list_client_id(id)
        return make_response(jsonify(client), status)
    
    # @client_owns_data(get_client_cpf) - O METODO PUT do client vai ficar desativado por enquanto
    # MOTIVO: NAME VEM DO USER, REGISTER DATE É AUTOMATICO, CPF É SÓ PRA CONFERIR SE BATE COM USER, NÂO TEM COMO MUDAR CPF.
    # def put(self, id):
    #     """Atualizar cliente por ID"""
    #     client_db, status = ClientService.list_client_id(id)
    #     if status != 200:
    #         return make_response(jsonify(client_db), status)
        
    #     try:
    #         schema_dto = ClientSchemaDTO().load(request.json)
    #         updated_client, status = ClientService.update(id, schema_dto)
    #         return make_response(jsonify(updated_client), status)
    #     except ValidationError as err:
    #         status_code = 400 if "missing" in str(err.messages).lower() else 422
    #         return {"error": err.messages}, status_code

    @role_required('admin')
    def delete(self, id):
        """Excluir cliente por ID"""

        response, status = ClientService.delete(id)
        return make_response(jsonify(response), status)

api.add_resource(ClientList, '/clients')
api.add_resource(ClientDetail, '/clients/<int:id>')
