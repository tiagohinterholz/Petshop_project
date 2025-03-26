from backend_app import db
import enum
from passlib.hash import pbkdf2_sha256

class ProfileEnum(enum.Enum):
    CLIENT = 'client'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.Enum(ProfileEnum, name='profile_enum'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    
    def encrypt_password(self):
        self.password = pbkdf2_sha256.hash(self.password)
    
    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)