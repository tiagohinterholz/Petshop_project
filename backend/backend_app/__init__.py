import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Inicializa as extensões, mas sem associar a nenhum app ainda
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
api = Api()
jwt = JWTManager()

TOKEN_BLACKLIST = set()  # Define a blacklist global

@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header, jwt_data):
    """Verifica se um token está na blacklist antes de validar a requisição."""
    return jwt_data["jti"] in TOKEN_BLACKLIST

def create_app(env="development"):
    """Cria e configura o aplicativo Flask"""
    app = Flask(__name__, static_folder='static')

    env = os.getenv("FLASK_ENV", "development")
    os.environ["TESTING"] = "True" if env == "testing" else "False"

    # Carrega a configuração correta
    if env == "testing":
        from backend_app.config_test import TestConfig
        app.config.from_object(TestConfig)
    else:
        from backend_app.config import Config
        app.config.from_object(Config)

    # Inicializa as extensões com o app configurado
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
        
    # Registro de rotas
    from .controller import (
        appointment_controller,
        address_controller,
        breed_controller,
        client_controller,
        contact_controller,
        forgot_password_controller,
        login_controller,
        logout_controller,
        pet_controller,
        refresh_token_controller,
        reset_password_controller,
        user_controller
    )
    
    api.init_app(app)
    
    # Configuração Swagger
    SWAGGER_URL = '/apidocs'
    API_URL = '/static/openapi.yaml'

    swagger_ui = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Petshop API"
        }
    )

    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)
             
    from .models import (
        breed_model, 
        client_model, 
        contact_model, 
        address_model, 
        pet_model, 
        appointment_model, 
        user_model
    )
        
    return app