from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app import api
from backend.backend_app.services.login_service import authenticate_user, get_current_user
from flask_jwt_extended import jwt_required

class Login(Resource):
    def post(self):
        """Autentica usuário e gera um token"""
        tokens, status = authenticate_user(request.json)  
        return make_response(jsonify(tokens), status)  

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        """Retorna dados do usuário autenticado"""
        response, status = get_current_user()
        return make_response(jsonify(response), status)

api.add_resource(Login, '/login')
api.add_resource(UserProfile, '/profile')