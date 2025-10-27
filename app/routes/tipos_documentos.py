from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from models import TiposDocumentos
from sqlalchemy import func
import re

tipos_documentos_bp = Blueprint('tipos_documentos', __name__, url_prefix='/tipos-documentos')

def validar_id(id_str):
    """Validar ID del tipo de documento"""
    if not id_str or not id_str.strip():
        return False, 'El ID es obligatorio'
    
    try:
        id_num = int(id_str)
    except ValueError:
        return False, 'El ID debe ser un número entero'
    
    if id_num <= 0:
        return False, 'El ID debe ser un número positivo'
    
    if id_num > 9999:
        return False, 'El ID no puede exceder 9999'
    
    return True, None

def validar_nombre(nombre):
    """Validar nombre del tipo de documento"""
    if not nombre or not nombre.strip():
        return False, 'El nombre es obligatorio'
    
    if len(nombre.strip()) < 2:
        return False, 'El nombre debe tener al menos 2 caracteres'
    
    if len(nombre.strip()) > 50:
        return False, 'El nombre no puede exceder 50 caracteres'
    
    # Validar que no contenga solo espacios o caracteres especiales
    if not re.match(r'^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ\s\-\.]+$', nombre):
        return False, 'El nombre solo puede contener letras, números, espacios, guiones y puntos'
    
    return True, None

def validar_descripcion(descripcion):
    """Validar descripción del tipo de documento"""
    if descripcion and len(descripcion.strip()) > 150:
        return False, 'La descripción no puede exceder 150 caracteres'
    
    return True, None

# READ - Listar todos los tipos de documentos
@tipos_documentos_bp.route('/')
@login_required
def listar():
    tipos = db.session.query(TiposDocumentos).order_by(TiposDocumentos.nombre).all()
    return render_template('tipos_documentos/listar.html', tipos=tipos)

# CREATE - Mostrar formulario de creación
@tipos_documentos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        try:
            id_tipo_documento_str = request.form.get('id_tipo_documento', '').strip()
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            activo = request.form.get('activo') == 'on'
            
            # Validar ID
            valido, error = validar_id(id_tipo_documento_str)
            if not valido:
                flash(error, 'error')
                return render_template('tipos_documentos/form.html')
            
            id_tipo_documento = int(id_tipo_documento_str)
            
            # Verificar si ya existe un tipo con ese ID
            existe_id = db.session.get(TiposDocumentos, id_tipo_documento)
            if existe_id:
                flash(f'Ya existe un tipo de documento con el ID {id_tipo_documento}.', 'error')
                return render_template('tipos_documentos/form.html')
            
            # Validar nombre
            valido, error = validar_nombre(nombre)
            if not valido:
                flash(error, 'error')
                return render_template('tipos_documentos/form.html')
            
            # Verificar si ya existe un tipo con ese nombre (case-insensitive)
            existe_nombre = db.session.query(TiposDocumentos).filter(
                func.lower(TiposDocumentos.nombre) == nombre.lower()
            ).first()
            
            if existe_nombre:
                flash(f'Ya existe un tipo de documento con el nombre "{nombre}".', 'error')
                return render_template('tipos_documentos/form.html')
            
            # Validar descripción
            valido, error = validar_descripcion(descripcion)
            if not valido:
                flash(error, 'error')
                return render_template('tipos_documentos/form.html')
            
            # Crear tipo de documento
            nuevo_tipo = TiposDocumentos(
                id_tipo_documento=id_tipo_documento,
                nombre=nombre.strip().title(),  # Capitalizar
                descripcion=descripcion.strip() if descripcion else None,
                activo=activo
            )
            
            db.session.add(nuevo_tipo)
            db.session.commit()
            
            flash(f'Tipo de documento "{nombre}" creado exitosamente.', 'success')
            return redirect(url_for('tipos_documentos.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear tipo de documento: {str(e)}', 'error')
    
    return render_template('tipos_documentos/form.html', tipo=None)

# UPDATE - Mostrar formulario de edición
@tipos_documentos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    tipo = db.session.get(TiposDocumentos, id)
    if not tipo:
        flash('Tipo de documento no encontrado.', 'error')
        return redirect(url_for('tipos_documentos.listar'))
    
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            activo = request.form.get('activo') == 'on'
            
            # Validar nombre
            valido, error = validar_nombre(nombre)
            if not valido:
                flash(error, 'error')
                return render_template('tipos_documentos/form.html', tipo=tipo)
            
            # Verificar si ya existe otro tipo con ese nombre
            existe = db.session.query(TiposDocumentos).filter(
                func.lower(TiposDocumentos.nombre) == nombre.lower(),
                TiposDocumentos.id_tipo_documento != id
            ).first()
            
            if existe:
                flash(f'Ya existe otro tipo de documento con el nombre "{nombre}".', 'error')
                return render_template('tipos_documentos/form.html', tipo=tipo)
            
            # Validar descripción
            valido, error = validar_descripcion(descripcion)
            if not valido:
                flash(error, 'error')
                return render_template('tipos_documentos/form.html', tipo=tipo)
            
            # Actualizar datos (el ID no se puede cambiar)
            tipo.nombre = nombre.strip().title()  # Capitalizar
            tipo.descripcion = descripcion.strip() if descripcion else None
            tipo.activo = activo
            
            db.session.commit()
            flash(f'Tipo de documento "{nombre}" actualizado exitosamente.', 'success')
            return redirect(url_for('tipos_documentos.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar tipo de documento: {str(e)}', 'error')
    
    return render_template('tipos_documentos/form.html', tipo=tipo)

# DELETE - Eliminar tipo de documento
@tipos_documentos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        tipo = db.session.get(TiposDocumentos, id)
        if not tipo:
            flash('Tipo de documento no encontrado.', 'error')
            return redirect(url_for('tipos_documentos.listar'))
        
        # Verificar si tiene registros relacionados
        tiene_relaciones = False
        mensaje_relaciones = []
        
        if hasattr(tipo, 'Clientes_Documento') and tipo.Clientes_Documento:
            tiene_relaciones = True
            mensaje_relaciones.append(f'{len(tipo.Clientes_Documento)} cliente(s)')
        
        if hasattr(tipo, 'Empleados_Documento') and tipo.Empleados_Documento:
            tiene_relaciones = True
            mensaje_relaciones.append(f'{len(tipo.Empleados_Documento)} empleado(s)')
        
        if tiene_relaciones:
            flash(f'No se puede eliminar "{tipo.nombre}" porque está asociado a {" y ".join(mensaje_relaciones)}.', 'error')
            return redirect(url_for('tipos_documentos.listar'))
        
        nombre = tipo.nombre
        db.session.delete(tipo)
        db.session.commit()
        flash(f'Tipo de documento "{nombre}" eliminado exitosamente.', 'error')  # Red notification
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar tipo de documento: {str(e)}', 'error')
    
    return redirect(url_for('tipos_documentos.listar'))

# TOGGLE - Activar/Desactivar tipo de documento
@tipos_documentos_bp.route('/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_activo(id):
    try:
        tipo = db.session.get(TiposDocumentos, id)
        if not tipo:
            flash('Tipo de documento no encontrado.', 'error')
            return redirect(url_for('tipos_documentos.listar'))
        
        # Verificar si tiene registros asociados antes de desactivar
        if tipo.activo:  # Si está activo y queremos desactivar
            tiene_uso = False
            if hasattr(tipo, 'Clientes_Documento') and tipo.Clientes_Documento:
                tiene_uso = True
            if hasattr(tipo, 'Empleados_Documento') and tipo.Empleados_Documento:
                tiene_uso = True
            
            if tiene_uso:
                flash(f'Advertencia: El tipo "{tipo.nombre}" tiene documentos asociados. Al desactivarlo, no estará disponible para nuevos registros.', 'warning')
        
        tipo.activo = not tipo.activo
        estado = "activado" if tipo.activo else "desactivado"
        
        db.session.commit()
        
        # Usar categoría apropiada
        categoria = 'success' if tipo.activo else 'warning'
        flash(f'Tipo de documento "{tipo.nombre}" {estado} exitosamente.', categoria)
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado: {str(e)}', 'error')
    
    return redirect(url_for('tipos_documentos.listar'))