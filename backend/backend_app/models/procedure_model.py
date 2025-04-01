from backend_app import db

class Procedure(db.Model):
    __tablename__= 'procedure'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    time_service = db.Column(db.Integer, nullable=False)  # duração do serviço em minutos