from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from models import TiposDocumentos
from sqlalchemy import func

tipos_documentos_bp = Blueprint('tipos_documentos', __name__, url_prefix='/tipos-documentos')

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
            id_tipo_documento = request.form.get('id_tipo_documento', '').strip()
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            activo = request.form.get('activo') == 'on'
            
            # Validaciones del ID
            if not id_tipo_documento:
                flash('El ID del tipo de documento es obligatorio.', 'error')
                return render_template('tipos_documentos/form.html')
            
            try:
                id_tipo_documento = int(id_tipo_documento)
            except ValueError:
                flash('El ID debe ser un número entero.', 'error')
                return render_template('tipos_documentos/form.html')
            
            if id_tipo_documento <= 0:
                flash('El ID debe ser un número positivo.', 'error')
                return render_template('tipos_documentos/form.html')
            
            # Verificar si ya existe un tipo con ese ID
            existe_id = db.session.get(TiposDocumentos, id_tipo_documento)
            if existe_id:
                flash(f'Ya existe un tipo de documento con el ID {id_tipo_documento}.', 'error')
                return render_template('tipos_documentos/form.html')
            
            # Validaciones del nombre
            if not nombre:
                flash('El nombre es obligatorio.', 'error')
                return render_template('tipos_documentos/form.html')
            
            if len(nombre) > 50:
                flash('El nombre no puede exceder 50 caracteres.', 'error')
                return render_template('tipos_documentos/form.html')
            
            # Verificar si ya existe un tipo con ese nombre
            existe_nombre = db.session.query(TiposDocumentos).filter(
                func.lower(TiposDocumentos.nombre) == nombre.lower()
            ).first()
            
            if existe_nombre:
                flash(f'Ya existe un tipo de documento con el nombre "{nombre}".', 'error')
                return render_template('tipos_documentos/form.html')
            
            # Crear tipo de documento
            nuevo_tipo = TiposDocumentos(
                id_tipo_documento=id_tipo_documento,
                nombre=nombre,
                descripcion=descripcion if descripcion else None,
                activo=activo
            )
            
            db.session.add(nuevo_tipo)
            db.session.commit()
            
            flash(f'Tipo de documento "{nombre}" creado exitosamente con ID {id_tipo_documento}.', 'success')
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
            
            # Validaciones
            if not nombre:
                flash('El nombre es obligatorio.', 'error')
                return render_template('tipos_documentos/form.html', tipo=tipo)
            
            if len(nombre) > 50:
                flash('El nombre no puede exceder 50 caracteres.', 'error')
                return render_template('tipos_documentos/form.html', tipo=tipo)
            
            # Verificar si ya existe otro tipo con ese nombre
            existe = db.session.query(TiposDocumentos).filter(
                func.lower(TiposDocumentos.nombre) == nombre.lower(),
                TiposDocumentos.id_tipo_documento != id
            ).first()
            
            if existe:
                flash(f'Ya existe otro tipo de documento con el nombre "{nombre}".', 'error')
                return render_template('tipos_documentos/form.html', tipo=tipo)
            
            # Actualizar datos (el ID no se puede cambiar)
            tipo.nombre = nombre
            tipo.descripcion = descripcion if descripcion else None
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
        if tipo.Clientes_Documento or tipo.Empleados_Documento:
            flash('No se puede eliminar este tipo de documento porque tiene registros asociados.', 'error')
            return redirect(url_for('tipos_documentos.listar'))
        
        nombre = tipo.nombre
        db.session.delete(tipo)
        db.session.commit()
        flash(f'Tipo de documento "{nombre}" eliminado exitosamente.', 'success')
        
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
        
        tipo.activo = not tipo.activo
        estado = "activado" if tipo.activo else "desactivado"
        
        db.session.commit()
        flash(f'Tipo de documento "{tipo.nombre}" {estado} exitosamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado: {str(e)}', 'error')
    
    return redirect(url_for('tipos_documentos.listar'))