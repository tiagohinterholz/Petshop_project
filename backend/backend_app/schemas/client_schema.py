from backend_app import ma, db
from backend_app.models.client_model import Client, User
from marshmallow import fields, validates, ValidationError

class ClientSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Client
        load_instance = True
        fields = ("id", "name", "cpf", "register_date")
    
    name = fields.String(required=True)
    cpf = fields.String(required=True, metadata={"unique": True})
    register_date = fields.Date(required=True)
    
    @validates('cpf')
    def validate_cpf(self, value):
        existing_client = db.session.query(Client).filter_by(cpf=value).first()
        if existing_client: # verifica se ja existe CPF cadastrado
            raise ValidationError("CPF já cadastrado para outro cliente.")

        existing_user = db.session.query(User).filter_by(cpf=value).first()
        if not existing_user: # veriffica se existe um CPF livre como USER mas nao como CLIENT para fazer o cadastro
            raise ValidationError("Não existe um usuário cadastrado com esse CPF.")