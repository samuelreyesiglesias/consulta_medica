from models.db import db

class Medico(db.Model):
    __tablename__ = 'Medico'

    id_medico = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('Especialidad.id_especialidad'), nullable=False)

    citas = db.relationship('Cita', backref='medico', lazy=True) 
