from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from backend_app import api

TOKEN_BLACKLIST = set()  # Conjunto para armazenar tokens inválidos

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  # Identificador único do token
        TOKEN_BLACKLIST.add(jti)  # Adiciona o token à blacklist
        return jsonify({"detail": "Logout realizado com sucesso."})

api.add_resource(LogoutResource, '/logout')