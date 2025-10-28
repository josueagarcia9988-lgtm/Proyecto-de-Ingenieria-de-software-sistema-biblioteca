import os
import secrets

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

    # Pepper secret para encriptación de contraseñas
    # IMPORTANTE: Genera una clave única y NUNCA la cambies después de tener usuarios
    # Para generar una nueva: python -c "import secrets; print(secrets.token_hex(32))"
    PEPPER_SECRET = os.environ.get('PEPPER_SECRET') or '0ec68042c99439c9cb759e6150bc0306492a4362c4e4fba79a3ec932e41d9bfd'
    # ⚠️ REEMPLAZA el valor por defecto con uno generado usando el comando de arriba