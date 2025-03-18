from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app.services.refresh_token_service import generate_refresh_token
from backend_app import api
from flasgger import swag_from

class RefreshToken(Resource):
    def post(self):
        """Gera um novo refresh token"""
        response, status = generate_refresh_token(request.json)
        return make_response(jsonify(response), status)

api.add_resource(RefreshToken, '/refresh-token')
