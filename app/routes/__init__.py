from flask import Blueprint, render_template
from flask_login import current_user

# Crear el blueprint principal
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Main route - shows landing or dashboard based on login status"""
    if current_user.is_authenticated:
        # Usuario logueado -> mostrar dashboard
        return render_template('dashboard.html')
    else:
        # Usuario NO logueado -> mostrar landing page
        return render_template('landing.html')

@main.route('/libros')
def libros():
    return "Aquí irán los libros"

@main.route('/clientes')
def usuarios():
    return "Aquí irán los usuarios"