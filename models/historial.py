from models.db import db

class Historial(db.Model):
    __tablename__ = 'Historial'

    id_historial = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('Paciente.id_paciente'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('Medico.id_medico'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.Text)

    paciente = db.relationship('Paciente', backref='historiales', lazy=True)
    medico = db.relationship('Medico', backref='historiales', lazy=True)
