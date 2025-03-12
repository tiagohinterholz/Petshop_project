from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app.services.forgot_password_service import forgot_password
from backend_app import api

class ForgotPassword(Resource):
    def post(self):
        """Gera um token de recuperação de senha e envia por e-mail."""
        response, status = forgot_password(request.json)
        return make_response(jsonify(response), status)

api.add_resource(ForgotPassword, '/forgot-password')