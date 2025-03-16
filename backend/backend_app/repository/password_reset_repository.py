from backend_app import db
from backend_app.models.password_reset_model import PasswordReset
import datetime

class PasswordResetRepository:
    
    @staticmethod
    def create(user_cpf, token):
        """Cria um novo registro de reset de senha"""
        reset_entry = PasswordReset(user_cpf=user_cpf, token=token)
        db.session.add(reset_entry)
        db.session.commit()
        return reset_entry

    @staticmethod
    def get_by_token(token):
        """Busca um reset de senha pelo token"""
        return PasswordReset.query.filter_by(token=token).first()

    @staticmethod
    def mark_as_used(token):
        """Marca o token como utilizado"""
        reset_entry = PasswordResetRepository.get_by_token(token)
        if reset_entry:
            reset_entry.used = True
            db.session.commit()

    @staticmethod
    def delete_expired_tokens():
        """Remove tokens expirados do banco"""
        PasswordReset.query.filter(PasswordReset.expires_at < datetime.utcnow()).delete()
        db.session.commit()
