from flask import request, jsonify, make_response
from flask_restful import Resource
from backend_app.services.reset_password_service import reset_password
from backend_app.schema_dto.reset_password_schema_dto import ResetPasswordSchemaDTO
from backend_app import api
from marshmallow import ValidationError
from flasgger import swag_from

class ResetPassword(Resource):
    def post(self):
        """Redefine a senha do usuário usando o token de recuperação."""       
        try:
            schema_dto = ResetPasswordSchemaDTO().load(request.json)
            response, status = reset_password(schema_dto)
            return make_response(jsonify(response), status)
        except ValidationError as err:
            return {"error": err.messages}, 400
            

api.add_resource(ResetPassword, '/reset-password')
