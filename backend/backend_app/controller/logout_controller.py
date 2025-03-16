from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from backend_app import api, TOKEN_BLACKLIST  # Importa a blacklist

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        """Realiza logout do usuário invalidando o token atual"""
        jti = get_jwt()["jti"]  # Obtém o identificador único do token
        TOKEN_BLACKLIST.add(jti)  # Adiciona o token à blacklist
        return make_response(jsonify({"message": "Logout realizado com sucesso."}), 200)

api.add_resource(LogoutResource, '/logout')
