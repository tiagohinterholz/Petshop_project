from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from backend_app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app)
api = Api(app)
jwt = JWTManager(app)


#Registro de rotas
from .views import breed_view, client_view, contact_view, address_view, pet_view, appointment_view, user_view, auth_view   
from .models import breed_model, client_model, contact_model, address_model, pet_model, appointment_model, user_model  
