import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

# Carregar configuração correta baseado no ambiente
if os.getenv("TESTING") == "True":
    from config_test import TestConfig as Config
else:
    from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

# Registro de rotas
from .views import (
    address_view, 
    appointment_view, 
    breed_view, 
    client_view, 
    contact_view, 
    forgot_password_view, 
    login_view, 
    logout_view, 
    pet_view, 
    user_view, 
    refresh_token_view, 
    reset_password_view
)   

from .models import (
    breed_model, 
    client_model, 
    contact_model, 
    address_model, 
    pet_model, 
    appointment_model, 
    user_model
)
