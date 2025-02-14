from flask import jsonify, request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend_app import api
from backend_app.services.auth_service import authenticate_user, get_current_user

class Login(Resource):
    def post(self):
        """Autentica usuario e gera um token"""
        data = request.json
        cpf = data.get("cpf")
        password = data.get("password")
        
        token = authenticate_user(cpf, password)
        if not token:
            return make_response(jsonify({'error': "CPF ou senha inválidos"}), 401)

        return make_response(jsonify({'access_token': token}), 200)

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        """Retorna dados do user autenticado"""
        user = get_current_user()
        if not user:
            return make_response(jsonify({"error": "Usuário não encontrado"}), 404)
        
        return make_response(jsonify(user), 200)

api.add_resource(Login, '/login')
api.add_resource(UserProfile, '/profile')
    