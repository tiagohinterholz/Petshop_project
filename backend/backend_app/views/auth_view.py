from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend_app import api
from backend_app.services.auth_service import authenticate_user, get_current_user

class Login(Resource):
    def post(self):
        """Autentica usuário e gera um token"""
        data = request.json
        cpf = data.get("cpf")
        password = data.get("password")

        tokens = authenticate_user(cpf, password)
        if not tokens:
            return make_response(jsonify({'error': "CPF ou senha inválidos"}), 401)

        access_token, refresh_token = tokens
        return make_response(jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200)

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        """Retorna dados do usuário autenticado"""
        cpf = get_jwt_identity()  # CPF é apenas uma string
        user, status = get_current_user(cpf)  # Buscar no banco pelo CPF

        if status != 200:
            return make_response(jsonify(user), status)

        return make_response(jsonify({
            "cpf": user["cpf"],
            "name": user["name"],
            "profile": user["profile"]
        }), 200)

api.add_resource(Login, '/login')
api.add_resource(UserProfile, '/profile')
