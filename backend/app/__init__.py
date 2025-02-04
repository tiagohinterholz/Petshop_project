from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# from .models import 
# from .views import

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    Migrate(app, db)
    
    #Registro de rotas
    from app.routes import main
    app.register_blueprint(main)
    
    return app