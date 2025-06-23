from models.db import db

class Especialidad(db.Model):
    __tablename__ = 'Especialidad'
    #Camel case

    id_especialidad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    medicos = db.relationship('Medico', backref='especialidad', lazy=True)
