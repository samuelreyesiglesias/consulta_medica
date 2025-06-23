from models.db import db

class Paciente(db.Model):
    __tablename__ = 'Paciente'

    id_paciente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.Enum('masculino', 'femenino', 'otro'), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
