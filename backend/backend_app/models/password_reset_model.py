from backend_app import db
from datetime import datetime, timedelta

class PasswordReset(db.Model):
    __tablename__ = "password_reset"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_cpf = db.Column(db.String, db.ForeignKey("users.cpf"), nullable=False)
    token = db.Column(db.Text, unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(minutes=15))
    used = db.Column(db.Boolean, default=False)

    def __init__(self, user_cpf, token):
        self.user_cpf = user_cpf
        self.token = token
        self.expires_at = datetime.utcnow() + timedelta(minutes=15)
        self.used = False

    def is_expired(self):
        """Verifica se o token expirou"""
        return datetime.utcnow() > self.expires_at
