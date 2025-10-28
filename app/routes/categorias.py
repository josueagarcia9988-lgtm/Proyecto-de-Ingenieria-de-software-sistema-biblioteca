from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from models import Categorias
from sqlalchemy import func
import re

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

def validar_nombre(nombre):
    """Validar nombre de categoría"""
    if not nombre or not nombre.strip():
        return False, 'El nombre es obligatorio'
    
    if len(nombre.strip()) < 2:
        return False, 'El nombre debe tener al menos 2 caracteres'
    
    if len(nombre.strip()) > 50:
        return False, 'El nombre no puede exceder 50 caracteres'
    
    # Validar que contenga al menos algunas letras
    if not re.search(r'[A-Za-zÁÉÍÓÚáéíóúÑñ]', nombre):
        return False, 'El nombre debe contener al menos algunas letras'
    
    return True, None

def validar_descripcion(descripcion):
    """Validar descripción de categoría"""
    if descripcion and len(descripcion.strip()) > 200:
        return False, 'La descripción no puede exceder 200 caracteres'
    
    return True, None

def get_next_id():
    """Obtener el siguiente ID disponible para categorías"""
    ultimo_id = db.session.query(func.max(Categorias.id_categoria)).scalar()
    return (ultimo_id or 0) + 1

# READ - Listar todas las categorías
@categorias_bp.route('/')
@login_required
def listar():
    categorias = db.session.query(Categorias).order_by(Categorias.nombre).all()
    return render_template('categorias/listar.html', categorias=categorias)

# CREATE - Mostrar formulario de creación
@categorias_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            observaciones = request.form.get('observaciones', '').strip()
            
            # Validar nombre
            valido, error = validar_nombre(nombre)
            if not valido:
                flash(error, 'error')
                return render_template('categorias/form.html')
            
            # Validar descripción
            valido, error = validar_descripcion(descripcion)
            if not valido:
                flash(error, 'error')
                return render_template('categorias/form.html')
            
            # Verificar nombre único (case-insensitive)
            categoria_existe = db.session.query(Categorias).filter(
                func.lower(Categorias.nombre) == nombre.lower()
            ).first()
            
            if categoria_existe:
                flash(f'Ya existe una categoría con el nombre "{nombre}".', 'error')
                return render_template('categorias/form.html')
            
            # Crear categoría
            nuevo_id = get_next_id()
            
            nueva_categoria = Categorias(
                id_categoria=nuevo_id,
                nombre=nombre.strip().title(),  # Capitalizar
                descripcion=descripcion.strip() if descripcion else None,
                observaciones=observaciones.strip() if observaciones else None
            )
            
            db.session.add(nueva_categoria)
            db.session.commit()
            
            flash(f'Categoría "{nombre}" creada exitosamente.', 'success')
            return redirect(url_for('categorias.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear categoría: {str(e)}', 'error')
    
    return render_template('categorias/form.html', categoria=None)

# UPDATE - Mostrar formulario de edición
@categorias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    categoria = db.session.get(Categorias, id)
    if not categoria:
        flash('Categoría no encontrada.', 'error')
        return redirect(url_for('categorias.listar'))
    
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            observaciones = request.form.get('observaciones', '').strip()
            
            # Validar nombre
            valido, error = validar_nombre(nombre)
            if not valido:
                flash(error, 'error')
                return render_template('categorias/form.html', categoria=categoria)
            
            # Validar descripción
            valido, error = validar_descripcion(descripcion)
            if not valido:
                flash(error, 'error')
                return render_template('categorias/form.html', categoria=categoria)
            
            # Verificar nombre único (excepto la categoría actual, case-insensitive)
            categoria_existe = db.session.query(Categorias).filter(
                func.lower(Categorias.nombre) == nombre.lower(),
                Categorias.id_categoria != id
            ).first()
            
            if categoria_existe:
                flash(f'Ya existe otra categoría con el nombre "{nombre}".', 'error')
                return render_template('categorias/form.html', categoria=categoria)
            
            # Actualizar datos
            categoria.nombre = nombre.strip().title()  # Capitalizar
            categoria.descripcion = descripcion.strip() if descripcion else None
            categoria.observaciones = observaciones.strip() if observaciones else None
            
            db.session.commit()
            flash(f'Categoría "{nombre}" actualizada exitosamente.', 'success')
            return redirect(url_for('categorias.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar categoría: {str(e)}', 'error')
    
    return render_template('categorias/form.html', categoria=categoria)

# DELETE - Eliminar categoría
@categorias_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        categoria = db.session.get(Categorias, id)
        if not categoria:
            flash('Categoría no encontrada.', 'error')
            return redirect(url_for('categorias.listar'))
        
        # Verificar si tiene libros asociados
        libros_count = 0
        if hasattr(categoria, 'Libro_Categoria') and categoria.Libro_Categoria:
            libros_count = len(categoria.Libro_Categoria)
        
        if libros_count > 0:
            flash(f'No se puede eliminar "{categoria.nombre}" porque tiene {libros_count} libro(s) asociado(s).', 'error')
            return redirect(url_for('categorias.listar'))
        
        nombre = categoria.nombre
        db.session.delete(categoria)
        db.session.commit()
        flash(f'Categoría "{nombre}" eliminada exitosamente.', 'error')  # Red notification
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar categoría: {str(e)}', 'error')
    
    return redirect(url_for('categorias.listar'))