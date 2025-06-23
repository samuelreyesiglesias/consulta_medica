from models.db import db

class Usuario(db.Model):
    __tablename__ = 'Usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('admin', 'medico', 'recepcionista'), nullable=False)
