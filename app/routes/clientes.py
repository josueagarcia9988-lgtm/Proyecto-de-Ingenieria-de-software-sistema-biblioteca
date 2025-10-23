from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Clientes
from bcrypt import hashpw, gensalt
from datetime import datetime
from sqlalchemy import func
import re

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

def validar_solo_letras(texto, campo):
    """Validar que un campo solo contenga letras y espacios"""
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', texto):
        return False, f'{campo} solo puede contener letras y espacios'
    return True, None

def get_next_id():
    """Obtener el siguiente ID disponible para clientes"""
    ultimo_id = db.session.query(func.max(Clientes.id_cliente)).scalar()
    return (ultimo_id or 0) + 1

# READ - Listar todos los clientes
@clientes_bp.route('/')
@login_required
def listar():
    clientes = db.session.query(Clientes).all()
    return render_template('clientes/listar.html', clientes=clientes)

# CREATE - Mostrar formulario de creación
@clientes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        try:
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            email = request.form.get('email', '').strip()
            
            # Validaciones
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html')
            
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html')
            
            # Verificar email duplicado
            email_existe = db.session.query(Clientes).filter_by(email=email).first()
            if email_existe:
                flash('Este email ya está registrado.', 'error')
                return render_template('clientes/form.html')
            
            # Crear cliente
            nuevo_id = get_next_id()
            password_hash = hashpw(request.form.get('password').encode('utf-8'), gensalt()).decode('utf-8')
            
            nuevo_cliente = Clientes(
                id_cliente=nuevo_id,
                nombres=nombres,
                apellidos=apellidos,
                email=email,
                password_hash=password_hash,
                telefono=request.form.get('telefono', 'No especificado'),
                direccion=request.form.get('direccion', 'No especificada'),
                tipo_usuario=request.form.get('tipo_usuario', 'cliente'),
                fecha_registro=datetime.now(),
                activo=int(request.form.get('activo', 1)),
                ot=int(request.form.get('ot', 0)),
                observaciones=request.form.get('observaciones', '')
            )
            
            db.session.add(nuevo_cliente)
            db.session.commit()
            
            flash('Cliente creado exitosamente.', 'success')
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
            
            # Validaciones
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html', cliente=cliente)
            
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('clientes/form.html', cliente=cliente)
            
            # Actualizar datos
            cliente.nombres = nombres
            cliente.apellidos = apellidos
            cliente.telefono = request.form.get('telefono', 'No especificado')
            cliente.direccion = request.form.get('direccion', 'No especificada')
            cliente.tipo_usuario = request.form.get('tipo_usuario', 'cliente')
            cliente.activo = int(request.form.get('activo', 1))
            cliente.ot = int(request.form.get('ot', 0))
            cliente.observaciones = request.form.get('observaciones', '')
            
            # Actualizar contraseña solo si se proporciona una nueva
            nueva_password = request.form.get('password')
            if nueva_password:
                cliente.password_hash = hashpw(nueva_password.encode('utf-8'), gensalt()).decode('utf-8')
            
            db.session.commit()
            flash('Cliente actualizado exitosamente.', 'success')
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
        
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente eliminado exitosamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cliente: {str(e)}', 'error')
    
    return redirect(url_for('clientes.listar'))