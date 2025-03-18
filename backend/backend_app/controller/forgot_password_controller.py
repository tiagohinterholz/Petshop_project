from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app.services.forgot_password_service import forgot_password
from backend_app.schema_dto.forgot_password_schema_dto import ForgotPasswordSchemaDTO
from backend_app import api
from marshmallow import ValidationError
class ForgotPassword(Resource):
    def post(self):
        """Gera um token de recuperação de senha e envia por e-mail."""
        try:
            schema_dto = ForgotPasswordSchemaDTO().load(request.json)
            response, status = forgot_password(schema_dto)
            return make_response(jsonify(response), status)
        except ValidationError as err:
            return {"error": err.messages}, 400
        
api.add_resource(ForgotPassword, '/forgot-password')