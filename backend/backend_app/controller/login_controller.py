from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend_app.services.login_service import authenticate_user, get_current_user
from flask_jwt_extended import jwt_required
from backend_app.schema_dto.login_schema_dto import LoginSchemaDTO
from marshmallow import ValidationError
from flasgger import swag_from

class Login(Resource):
    def post(self):
        try:
            schema_dto = LoginSchemaDTO().load(request.json)
            """Autentica usuário e gera um token"""
            tokens, status = authenticate_user(schema_dto)  
            return make_response(jsonify(tokens), status)
        except ValidationError as err:
            return {"error": err.messages}, 400       

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        """Retorna dados do usuário autenticado"""
        response, status = get_current_user()
        return make_response(jsonify(response), status)

api.add_resource(Login, '/login')
api.add_resource(UserProfile, '/profile')