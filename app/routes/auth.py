from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from models import Clientes

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Buscar usuario por email
        usuario = db.session.query(Clientes).filter_by(email=email).first()
        
        # Verificar si existe y la contraseña es correcta
        if usuario and check_password_hash(usuario.password_hash, password):
            if usuario.activo:
                login_user(usuario)
                flash('¡Inicio de sesión exitoso!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Tu cuenta está inactiva.', 'error')
        else:
            flash('Email o contraseña incorrectos.', 'error')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))