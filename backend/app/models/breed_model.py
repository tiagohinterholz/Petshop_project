from app import db

class Breed(db.Model):
    __tablename__ = 'breed'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = db.Column(db.String(50), nullable=False)
    
    