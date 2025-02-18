from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from backend_app import api

class RefreshTokenList(Resource):
    
    @jwt_required(refresh=True)
    def post(self):
        """Gerar um novo access token a partir do refresh token"""
        identity = str(get_jwt_identity())
        new_access_token = create_access_token(identity=identity)
        
        return make_response(jsonify({'access_token': new_access_token}), 200)

api.add_resource(RefreshTokenList, '/token/refresh')
