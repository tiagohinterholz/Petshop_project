import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from backend_app.docs.swagger_config import swagger_config

# Inicializa as extensões, mas sem associar a nenhum app ainda
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
api = Api()
jwt = JWTManager()

def create_app(env="development"):
    """Cria e configura o aplicativo Flask"""
    app = Flask(__name__)

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
    swagger = Swagger(app, config=swagger_config)
    
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