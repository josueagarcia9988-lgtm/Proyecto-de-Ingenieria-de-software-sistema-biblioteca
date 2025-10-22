from flask import Blueprint, render_template

# Crear el blueprint principal
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/libros')
def libros():
    return "Aquí irán los libros"

@main.route('/clientes')
def usuarios():
    return "Aquí irán los usuarios"
