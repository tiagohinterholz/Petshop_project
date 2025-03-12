from backend_app import ma, db
from backend_app.models.appointment_model import Appointment

class AppointmentRepository:
    """Classe responsável pelo acesso ao banco de dados."""

    @staticmethod
    def list_all():
        """Lista todos os agendamentos."""
        return Appointment.query.all()

    @staticmethod
    def get_by_id(id):
        """Busca um agendamento pelo ID."""
        return db.session.get(Appointment, id)

    @staticmethod
    def create(validated_data):
        """Cria um novo agendamento."""
        new_appointment = Appointment(
            pet_id=validated_data["pet_id"],
            desc_appoint=validated_data["desc_appoint"],
            price=validated_data["price"],
            date_appoint=validated_data["date_appoint"]
            )
        db.session.add(new_appointment)
        db.session.commit()
        return new_appointment

    @staticmethod
    def update(appointment, new_data):
        """Atualiza um agendamento no banco de dados."""
        appointment.pet_id = new_data["pet_id"]
        appointment.desc_appoint = new_data["desc_appoint"]
        appointment.price = new_data["price"]
        appointment.date_appoint = new_data["date_appoint"]
        """Confirma as alterações no banco de dados."""
        db.session.commit()

    @staticmethod
    def delete(appointment):
        """Exclui um agendamento."""
        db.session.delete(appointment)
        db.session.commit()