from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.user_service import register_user, delete_user, list_user_id
from backend_app.schemas.user_schema import UserSchema

class UserList(Resource):   
    def post(self):        
        """Cadastrar novo user"""
              
        schema = UserSchema()
        errors = schema.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)
        
        user = schema.load(request.json)
        new_user = register_user(user)
        return make_response(schema.jsonify(new_user), 201)

class UserDetail(Resource):    
    def delete(self, cpf):
        """Excluir user por id"""
        user = list_user_id(cpf)
        if not cpf:
            return make_response(jsonify({'error': 'CPF não encontrado'}), 404)
        
        delete_user(cpf)
        return make_response('', 204)

api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<string:cpf>')