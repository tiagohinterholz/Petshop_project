from backend import db
from backend.models.client_model import Client
import enum

class ProfileEnum(enum.Enum):
    CLIENT = 'client'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__='user'
    cpf = db.Column(db.String(14), db.ForeignKey('client.cpf'), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.Enum(ProfileEnum, name='profile_enum'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    client = db.relationship(Client, backref=db.backref('user', uselist=False))