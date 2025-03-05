from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app.services.reset_password_service import reset_password
from backend_app import api

class ResetPassword(Resource):
    def post(self):
        """Redefine a senha do usuário usando o token de recuperação."""
        response, status = reset_password(request.json)
        return make_response(jsonify(response), status)

api.add_resource(ResetPassword, '/reset-password')
