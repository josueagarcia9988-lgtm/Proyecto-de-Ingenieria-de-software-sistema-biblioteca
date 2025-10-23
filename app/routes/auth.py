from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from bcrypt import hashpw, gensalt, checkpw
from app import db
from models import Clientes
from datetime import datetime
from sqlalchemy import func
import re

auth = Blueprint('auth', __name__)

def validar_solo_letras(texto, campo):
    """Validar que un campo solo contenga letras y espacios"""
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', texto):
        return False, f'{campo} solo puede contener letras y espacios'
    return True, None

def get_next_id():
    """Obtener el siguiente ID disponible para clientes"""
    ultimo_id = db.session.query(func.max(Clientes.id_cliente)).scalar()
    return (ultimo_id or 0) + 1

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # ← ADD THIS CHECK AT THE BEGINNING
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Buscar usuario por email
        usuario = db.session.query(Clientes).filter_by(email=email).first()
        
        # Verificar si existe y la contraseña es correcta
        if usuario and checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
            if usuario.activo:
                login_user(usuario)
                flash('¡Inicio de sesión exitoso!', 'success')
                return redirect(url_for('main.index'))  # ← CHANGED
            else:
                flash('Tu cuenta está inactiva.', 'error')
        else:
            flash('Email o contraseña incorrectos.', 'error')
    
    return render_template('login.html')

@auth.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            email = request.form.get('email', '').strip()
            
            # Validar nombres (solo letras)
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('registrar.html')
            
            # Validar apellidos (solo letras)
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('registrar.html')
            
            # Verificar si el email ya existe
            email_existe = db.session.query(Clientes).filter_by(email=request.form.get('email')).first()
            if email_existe:
                flash('Este email ya está registrado.', 'error')
                return render_template('registrar.html')
            
            # Verificar que las contraseñas coincidan
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            
            if password != password_confirm:
                flash('Las contraseñas no coinciden.', 'error')
                return render_template('registrar.html')
            
            # Obtener siguiente ID
            nuevo_id = get_next_id()
            
            # Hash de la contraseña con bcrypt
            password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            
            # Crear nuevo cliente con valores por defecto
            nuevo_cliente = Clientes(
                id_cliente=nuevo_id,
                nombres=request.form.get('nombres'),
                apellidos=request.form.get('apellidos'),
                email=request.form.get('email'),
                password_hash=password_hash,
                telefono=request.form.get('telefono', 'No especificado'),
                direccion='No especificada',
                tipo_usuario='cliente',
                fecha_registro=datetime.now(),
                activo=1,
                ot=0,
                observaciones=''
            )
            
            db.session.add(nuevo_cliente)
            db.session.commit()
            
            flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la cuenta: {str(e)}', 'error')
    
    return render_template('registrar.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))  # ← CHANGED (was 'auth.login')