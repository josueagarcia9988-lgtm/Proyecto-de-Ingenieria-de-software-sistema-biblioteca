from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import Clientes
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload
import re
import hashlib

auth = Blueprint('auth', __name__)

def hash_password(password):
    """
    Hash de contraseña completamente aleatorio y único:
    1. Genera una sal aleatoria única de 32 bytes
    2. HMAC con pepper + sal
    3. Bcrypt
    4. Almacena: sal_aleatoria + hash (todo en hex)
    Resultado: Cada hash comienza diferente
    """
    import hmac
    import secrets
    from bcrypt import hashpw, gensalt
    
    # Obtener pepper desde configuración
    try:
        pepper = current_app.config.get('PEPPER_SECRET', '')
    except RuntimeError:
        from config import Config
        pepper = Config.PEPPER_SECRET
    
    # Generar sal aleatoria única de 32 bytes
    random_salt = secrets.token_bytes(32)
    
    # HMAC con pepper + sal aleatoria
    hmac_hash = hmac.new(
        (pepper + random_salt.hex()).encode('utf-8'),
        password.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    # Bcrypt sobre el HMAC
    bcrypt_hash = hashpw(hmac_hash, gensalt(rounds=12))
    
    # Combinar: sal_aleatoria + bcrypt_hash, todo en hexadecimal
    # La sal aleatoria va primero (64 caracteres hex = 32 bytes)
    final_hash = random_salt.hex() + bcrypt_hash.hex()
    
    return final_hash

def verify_password(password, stored_hash):
    """
    Verificar contraseña con el mismo proceso usado en hash_password
    """
    try:
        import hmac
        from bcrypt import checkpw
        
        # Obtener pepper desde configuración
        try:
            pepper = current_app.config.get('PEPPER_SECRET', '')
        except RuntimeError:
            from config import Config
            pepper = Config.PEPPER_SECRET
        
        # Extraer la sal aleatoria (primeros 64 caracteres hex = 32 bytes)
        random_salt_hex = stored_hash[:64]
        bcrypt_hash_hex = stored_hash[64:]
        
        # Convertir de hex a bytes
        random_salt = bytes.fromhex(random_salt_hex)
        bcrypt_hash = bytes.fromhex(bcrypt_hash_hex)
        
        # Recrear el HMAC con la misma sal aleatoria
        hmac_hash = hmac.new(
            (pepper + random_salt_hex).encode('utf-8'),
            password.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # Verificar con bcrypt
        return checkpw(hmac_hash, bcrypt_hash)
        
    except Exception as e:
        print(f"Error verificando contraseña: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def validar_solo_letras(texto, campo):
    """Validar que un campo solo contenga letras y espacios"""
    if not texto or not texto.strip():
        return False, f'{campo} es obligatorio'
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', texto):
        return False, f'{campo} solo puede contener letras y espacios'
    if len(texto.strip()) < 2:
        return False, f'{campo} debe tener al menos 2 caracteres'
    if len(texto.strip()) > 50:
        return False, f'{campo} no puede exceder 50 caracteres'
    return True, None

def validar_email(email):
    """Validar formato de email"""
    if not email or not email.strip():
        return False, 'Email es obligatorio'
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, 'Formato de email inválido'
    if len(email) > 100:
        return False, 'Email no puede exceder 100 caracteres'
    return True, None

def validar_telefono(telefono):
    """Validar formato de teléfono"""
    if not telefono or telefono == 'No especificado':
        return True, None
    pattern = r'^[\d\s\-\+\(\)]{8,20}$'
    if not re.match(pattern, telefono):
        return False, 'Formato de teléfono inválido (ej: 9999-9999)'
    return True, None

def validar_password(password, confirmar=None):
    """Validar contraseña"""
    if not password:
        return False, 'Contraseña es obligatoria'
    if len(password) < 6:
        return False, 'Contraseña debe tener al menos 6 caracteres'
    if len(password) > 100:
        return False, 'Contraseña no puede exceder 100 caracteres'
    if confirmar is not None and password != confirmar:
        return False, 'Las contraseñas no coinciden'
    return True, None

def get_next_id():
    """Obtener el siguiente ID disponible para clientes"""
    ultimo_id = db.session.query(func.max(Clientes.id_cliente)).scalar()
    return (ultimo_id or 0) + 1

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('login.html')
        
        # Buscar usuario por email (case-insensitive)
        usuario = db.session.query(Clientes).filter(
            func.lower(Clientes.email) == email
        ).first()
        
        # Verificar si existe y la contraseña es correcta
        if usuario and verify_password(password, usuario.password_hash):
            # Verificar estado del usuario
            if hasattr(usuario, 'Estado_Usuarios') and usuario.Estado_Usuarios:
                estado = usuario.Estado_Usuarios
                
                # Verificar si el estado permite login
                if not estado.permite_login:
                    flash(f'Tu cuenta está {estado.nombre}. No puedes acceder al sistema.', 'error')
                    return render_template('login.html')
                
                # Si el estado es "Pendiente cambio de contraseña" (id_estado == 4)
                if usuario.id_estado == 4:
                    flash('Debes cambiar tu contraseña antes de continuar.', 'warning')
                    return render_template('login.html')
            
            # Login exitoso
            login_user(usuario)
            flash(f'¡Bienvenido, {usuario.nombres}!', 'success')
            
            # Redirect to next page if exists, otherwise to index
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Email o contraseña incorrectos.', 'error')
    
    return render_template('login.html')

@auth.route('/registrar', methods=['GET', 'POST'])
def registrar():
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            email = request.form.get('email', '').strip().lower()
            telefono = request.form.get('telefono', '').strip()
            password = request.form.get('password', '')
            password_confirm = request.form.get('password_confirm', '')
            
            # Validar nombres
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('registrar.html')
            
            # Validar apellidos
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('registrar.html')
            
            # Validar email
            valido, error = validar_email(email)
            if not valido:
                flash(error, 'error')
                return render_template('registrar.html')
            
            # Verificar si el email ya existe (case-insensitive)
            email_existe = db.session.query(Clientes).filter(
                func.lower(Clientes.email) == email
            ).first()
            
            if email_existe:
                flash('Este email ya está registrado.', 'error')
                return render_template('registrar.html')
            
            # Validar teléfono
            valido, error = validar_telefono(telefono)
            if not valido:
                flash(error, 'error')
                return render_template('registrar.html')
            
            # Validar contraseña
            valido, error = validar_password(password, password_confirm)
            if not valido:
                flash(error, 'error')
                return render_template('registrar.html')
            
            # Obtener siguiente ID
            nuevo_id = get_next_id()
            
            # Hash de la contraseña con método mejorado
            password_hash = hash_password(password)
            
            # Crear nuevo cliente
            nuevo_cliente = Clientes(
                id_cliente=nuevo_id,
                nombres=nombres.title(),
                apellidos=apellidos.title(),
                email=email,
                password_hash=password_hash,
                telefono=telefono if telefono else 'No especificado',
                direccion='No especificada',
                tipo_usuario='cliente',
                fecha_registro=datetime.now(),
                ot=0,
                id_estado=1,  # 1 = Activo
                observaciones=None
            )
            
            db.session.add(nuevo_cliente)
            db.session.commit()
            
            flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la cuenta: {str(e)}', 'error')
            print(f"Error en registro: {str(e)}")
    
    return render_template('registrar.html')

@auth.route('/logout')
@login_required
def logout():
    nombre = current_user.nombres
    logout_user()
    flash(f'Hasta pronto, {nombre}. Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))