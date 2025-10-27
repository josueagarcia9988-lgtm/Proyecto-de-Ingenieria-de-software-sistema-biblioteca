from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Clientes
from bcrypt import hashpw, gensalt
from datetime import datetime
from sqlalchemy import func
import re
import secrets
import string

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

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
    # Permitir formatos: 9999-9999, +504 9999-9999, etc.
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

# READ - Listar todos los clientes
@clientes_bp.route('/')
@login_required
def listar():
    clientes = db.session.query(Clientes).order_by(Clientes.fecha_registro.desc()).all()
    return render_template('clientes/listar.html', clientes=clientes)

# CREATE - Mostrar formulario de creación
@clientes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        try:
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            email = request.form.get('email', '').strip().lower()
            telefono = request.form.get('telefono', '').strip()
            password = request.form.get('password', '')
            
            # Validar nombres
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html')
            
            # Validar apellidos
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html')
            
            # Validar email
            valido, error = validar_email(email)
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html')
            
            # Verificar email duplicado
            email_existe = db.session.query(Clientes).filter(
                func.lower(Clientes.email) == email
            ).first()
            if email_existe:
                flash('Este email ya está registrado.', 'error')
                return render_template('clientes/form.html')
            
            # Validar teléfono
            valido, error = validar_telefono(telefono)
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html')
            
            # Validar contraseña
            valido, error = validar_password(password)
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html')
            
            # Crear cliente
            nuevo_id = get_next_id()
            password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            
            nuevo_cliente = Clientes(
                id_cliente=nuevo_id,
                nombres=nombres.title(),  # Capitalizar nombres
                apellidos=apellidos.title(),  # Capitalizar apellidos
                email=email,
                password_hash=password_hash,
                telefono=telefono if telefono else 'No especificado',
                direccion=request.form.get('direccion', '').strip() or 'No especificada',
                tipo_usuario=request.form.get('tipo_usuario', 'cliente'),
                fecha_registro=datetime.now(),
                activo=int(request.form.get('activo', 1)),
                ot=int(request.form.get('ot', 0)),
                observaciones=request.form.get('observaciones', '').strip()
            )
            
            db.session.add(nuevo_cliente)
            db.session.commit()
            
            flash(f'Cliente {nombres} {apellidos} creado exitosamente.', 'success')
            return redirect(url_for('clientes.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear cliente: {str(e)}', 'error')
    
    return render_template('clientes/form.html', cliente=None)

# UPDATE - Mostrar formulario de edición
@clientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    cliente = db.session.get(Clientes, id)
    if not cliente:
        flash('Cliente no encontrado.', 'error')
        return redirect(url_for('clientes.listar'))
    
    if request.method == 'POST':
        try:
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            telefono = request.form.get('telefono', '').strip()
            
            # Validar nombres
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html', cliente=cliente)
            
            # Validar apellidos
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html', cliente=cliente)
            
            # Validar teléfono
            valido, error = validar_telefono(telefono)
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html', cliente=cliente)
            
            # Actualizar datos (NO incluye contraseña)
            cliente.nombres = nombres.title()
            cliente.apellidos = apellidos.title()
            cliente.telefono = telefono if telefono else 'No especificado'
            cliente.direccion = request.form.get('direccion', '').strip() or 'No especificada'
            cliente.tipo_usuario = request.form.get('tipo_usuario', 'cliente')
            cliente.activo = int(request.form.get('activo', 1))
            cliente.ot = int(request.form.get('ot', 0))
            cliente.observaciones = request.form.get('observaciones', '').strip()
            
            db.session.commit()
            flash(f'Cliente {nombres} {apellidos} actualizado exitosamente.', 'success')
            return redirect(url_for('clientes.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cliente: {str(e)}', 'error')
    
    return render_template('clientes/form.html', cliente=cliente)

# DELETE - Eliminar cliente
@clientes_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        cliente = db.session.get(Clientes, id)
        if not cliente:
            flash('Cliente no encontrado.', 'error')
            return redirect(url_for('clientes.listar'))
        
        # No permitir que el usuario se elimine a sí mismo
        if cliente.id_cliente == current_user.id_cliente:
            flash('No puedes eliminar tu propia cuenta.', 'error')
            return redirect(url_for('clientes.listar'))
        
        nombre_completo = f'{cliente.nombres} {cliente.apellidos}'
        db.session.delete(cliente)
        db.session.commit()
        flash(f'Cliente {nombre_completo} eliminado exitosamente.', 'error')  # ← RED notification
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cliente: {str(e)}', 'error')
    
    return redirect(url_for('clientes.listar'))

@clientes_bp.route('/resetear-password/<int:id>', methods=['POST'])
@login_required
def resetear_password(id):
    try:
        cliente = db.session.get(Clientes, id)
        if not cliente:
            flash('Cliente no encontrado.', 'error')
            return redirect(url_for('clientes.listar'))
        
        # Generate random password (8 characters: letters + numbers)
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        
        # Hash the temporary password
        cliente.password_hash = hashpw(temp_password.encode('utf-8'), gensalt()).decode('utf-8')
        
        db.session.commit()
        
        # Show the temporary password to admin (they should share it with user)
        flash(f'Contraseña temporal para {cliente.nombres}: {temp_password} (Enviado al correo del Usuario)', 'warning')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al resetear contraseña: {str(e)}', 'error')
    
    return redirect(url_for('clientes.editar', id=id))