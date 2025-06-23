from models.db import db

class Cita(db.Model):
    __tablename__ = 'Cita'

    id_cita = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('Paciente.id_paciente'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('Medico.id_medico'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Enum('pendiente', 'confirmada', 'cancelada', 'completada'), nullable=False)

    paciente = db.relationship('Paciente', backref='citas', lazy=True)
