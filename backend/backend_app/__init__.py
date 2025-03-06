import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

# Inicializa as extensões, mas sem associar a nenhum app ainda
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
api = Api()
jwt = JWTManager()

def create_app():
    """Cria e configura o aplicativo Flask"""
    app = Flask(__name__)

    # Carregar configuração correta baseado no ambiente
    if os.getenv("TESTING") == "True":
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