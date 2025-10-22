from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(Config)
    
    # Inicializar la base de datos con la app
    db.init_app(app)
    
    # Registrar blueprints (rutas)
    from app.routes import main
    app.register_blueprint(main)
    
    return app