import os

class Config:
    # Configuración general
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui-cambiala'
    
    # Configuración de la base de datos MSSQL
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://localhost:1433/libreria?'
        'driver=ODBC+Driver+17+for+SQL+Server&'
        'trusted_connection=yes'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False