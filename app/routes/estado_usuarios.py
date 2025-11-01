from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app import db
from models import EstadoUsuarios
from sqlalchemy import func

estado_usuarios_bp = Blueprint('estado_usuarios', __name__, url_prefix='/estado-usuarios')

def get_next_id():
    """Obtener el siguiente ID disponible para estados"""
    ultimo_id = db.session.query(func.max(EstadoUsuarios.id_estado)).scalar()
    return (ultimo_id or 0) + 1

# API para crear desde modal (PARA EL MODAL DENTRO DEL FORMULARIO)
@estado_usuarios_bp.route('/crear-rapido', methods=['POST'])
@login_required
def crear_rapido():
    """Crear estado desde modal - devuelve JSON"""
    try:
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        permite_login = int(request.form.get('permite_login', 0))
        
        # Validaciones
        if not nombre:
            return jsonify({'success': False, 'error': 'El nombre es obligatorio'}), 400
        
        if not descripcion:
            return jsonify({'success': False, 'error': 'La descripción es obligatoria'}), 400
        
        # Validar nombre único
        existe = db.session.query(EstadoUsuarios).filter_by(nombre=nombre).first()
        if existe:
            return jsonify({'success': False, 'error': 'Ya existe un estado con ese nombre'}), 400
        
        # Crear estado
        nuevo_id = get_next_id()
        nuevo_estado = EstadoUsuarios(
            id_estado=nuevo_id,
            nombre=nombre,
            descripcion=descripcion,
            permite_login=permite_login,
            observaciones=''
        )
        
        db.session.add(nuevo_estado)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'id_estado': nuevo_id,
            'nombre': nombre,
            'message': 'Estado creado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# CRUD completo - Listar
@estado_usuarios_bp.route('/')
@login_required
def listar():
    estados = db.session.query(EstadoUsuarios).all()
    return render_template('estado_usuarios/listar.html', estados=estados)

# CREATE - Formulario completo
@estado_usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            permite_login = int(request.form.get('permite_login', 0))
            
            # Validar nombre único
            existe = db.session.query(EstadoUsuarios).filter_by(nombre=nombre).first()
            if existe:
                flash('Ya existe un estado con ese nombre.', 'error')
                return render_template('estado_usuarios/form.html')
            
            nuevo_id = get_next_id()
            nuevo_estado = EstadoUsuarios(
                id_estado=nuevo_id,
                nombre=nombre,
                descripcion=descripcion,
                permite_login=permite_login,
                observaciones=request.form.get('observaciones', '')
            )
            
            db.session.add(nuevo_estado)
            db.session.commit()
            
            flash('Estado creado exitosamente.', 'success')
            return redirect(url_for('estado_usuarios.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear estado: {str(e)}', 'error')
    
    return render_template('estado_usuarios/form.html', estado=None)

# UPDATE
@estado_usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    estado = db.session.get(EstadoUsuarios, id)
    if not estado:
        flash('Estado no encontrado.', 'error')
        return redirect(url_for('estado_usuarios.listar'))
    
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            
            # Validar nombre único (excepto el actual)
            existe = db.session.query(EstadoUsuarios).filter(
                EstadoUsuarios.nombre == nombre,
                EstadoUsuarios.id_estado != id
            ).first()
            
            if existe:
                flash('Ya existe un estado con ese nombre.', 'error')
                return render_template('estado_usuarios/form.html', estado=estado)
            
            estado.nombre = nombre
            estado.descripcion = request.form.get('descripcion', '').strip()
            estado.permite_login = int(request.form.get('permite_login', 0))
            estado.observaciones = request.form.get('observaciones', '')
            
            db.session.commit()
            flash('Estado actualizado exitosamente.', 'success')
            return redirect(url_for('estado_usuarios.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar estado: {str(e)}', 'error')
    
    return render_template('estado_usuarios/form.html', estado=estado)

# DELETE
@estado_usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        estado = db.session.get(EstadoUsuarios, id)
        if not estado:
            flash('Estado no encontrado.', 'error')
            return redirect(url_for('estado_usuarios.listar'))
        
        # Verificar si tiene clientes asociados
        if estado.Clientes:
            flash(f'No se puede eliminar el estado "{estado.nombre}" porque tiene {len(estado.Clientes)} clientes asociados.', 'error')
            return redirect(url_for('estado_usuarios.listar'))
        
        db.session.delete(estado)
        db.session.commit()
        flash('Estado eliminado exitosamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar estado: {str(e)}', 'error')
    
    return redirect(url_for('estado_usuarios.listar'))