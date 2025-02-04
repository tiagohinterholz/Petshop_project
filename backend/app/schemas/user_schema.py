from app import ma
from app.models.user_model import User, ProfileEnum
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = User
        load_instance = True
        fields = ('cpf', 'name', 'profile', 'password')
    
    cpf = fields.String(required=True)
    name = fields.String(required=True)
    profile = fields.Enum(ProfileEnum, required=True)
    password = fields.String(required=True, load_only=True)
    
