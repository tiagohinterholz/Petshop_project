from backend_app import ma
from backend_app.models.user_model import User, ProfileEnum
from marshmallow import fields, validates, ValidationError
from backend_app import db

class UserSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = User
        load_instance = True
        fields = ('cpf', 'name', 'profile', 'password')
    
    cpf = fields.String(required=True, unique=True)
    name = fields.String(required=True)
    profile = fields.Enum(ProfileEnum, by_value=True, required=True)
    password = fields.String(required=True, load_only=True)
    
    @validates('profile')
    def validate_profile(self, value):
        if value == ProfileEnum.ADMIN:
            raise ValidationError("Não é permitido criar um usuário ADMIN")
    
    @validates('cpf')
    def validate_cpf(self, value):
        existing_user = db.session.get(User, value)
        if existing_user:
            raise ValidationError("Usuário já cadastrado com esse CPF")