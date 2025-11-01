from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicializar SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__, 
                static_folder='static',
                static_url_path='/static')
    
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
    from app.routes.clientes import clientes_bp
    from app.routes.autores import autores_bp
    from app.routes.tipos_documentos import tipos_documentos_bp
    from app.routes.categorias import categorias_bp
    from app.routes.estado_usuarios import estado_usuarios_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(autores_bp)
    app.register_blueprint(tipos_documentos_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(estado_usuarios_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import Clientes
    return db.session.get(Clientes, int(user_id))