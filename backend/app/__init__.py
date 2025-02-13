from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    ma.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    jwt = JWTManager(app)
    
    #Registro de rotas
    from backend.tests.routes import main
    app.register_blueprint(main)
    
    from app.models import (
        user_model, 
        pet_model, 
        client_model, 
        contact_model, 
        address_model, 
        appointment_model, 
        breed_model
    )
    
    return app