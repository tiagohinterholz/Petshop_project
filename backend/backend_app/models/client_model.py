from backend_app.models.user_model import User
from backend_app import db
from datetime import datetime, date

class Client(db.Model):
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    register_date = db.Column(db.Date, nullable=False)
    
    user = db.relationship("User", backref=db.backref("client", uselist=False), foreign_keys=[user_id])