from app import db

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    register_date = db.Column(db.Date, nullable=False)
    
    