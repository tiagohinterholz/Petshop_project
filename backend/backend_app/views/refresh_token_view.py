from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from backend_app import api
from backend_app.services.auth_service import get_current_user

class RefreshTokenList(Resource):
    
    @jwt_required(refresh=True)
    def post(self):
        """Refresh no token"""
        identity = str(get_jwt_identity())
        new_acess_token = create_access_token(identity=identity)
        
        if not new_acess_token:
            return make_response(jsonify({'error': "CPF ou senha inválidos"}), 401)
        
        return make_response({
            'access_token': new_acess_token,
        }, 200)

api.add_resource(RefreshTokenList, '/token/refresh')