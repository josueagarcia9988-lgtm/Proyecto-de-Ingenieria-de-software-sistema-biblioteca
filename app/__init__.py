from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicializar SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(Config)
    
    # Inicializar la base de datos con la app
    db.init_app(app)
    
    # Inicializar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Registrar blueprints (rutas)
    from app.routes import main
    from app.routes.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from models import Clientes
    return db.session.get(Clientes, int(user_id))