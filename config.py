# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/sistemasalud'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta'
