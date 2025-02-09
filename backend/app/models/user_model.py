from app import db
from app.models.client_model import Client
import enum
from passlib.hash import pbkdf2_sha256

class ProfileEnum(enum.Enum):
    CLIENT = 'client'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__='user'
    cpf = db.Column(db.String(14), db.ForeignKey('client.cpf'), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.Enum(ProfileEnum, name='profile_enum'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    client = db.relationship(Client, backref=db.backref('user', uselist=False))
    
    def encrypt_password(self):
        self.password = pbkdf2_sha256.hash(self.senha)
    
    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)