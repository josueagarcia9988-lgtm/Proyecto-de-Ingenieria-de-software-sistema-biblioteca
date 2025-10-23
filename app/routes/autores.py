from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from models import Autores
from datetime import datetime
from sqlalchemy import func
import re

autores_bp = Blueprint('autores', __name__, url_prefix='/autores')

def validar_solo_letras(texto, campo):
    """Validar que un campo solo contenga letras y espacios"""
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', texto):
        return False, f'{campo} solo puede contener letras y espacios'
    return True, None

def get_next_id():
    """Obtener el siguiente ID disponible para autores"""
    ultimo_id = db.session.query(func.max(Autores.id_autor)).scalar()
    return (ultimo_id or 0) + 1

# READ - Listar todos los autores
@autores_bp.route('/')
@login_required
def listar():
    autores = db.session.query(Autores).all()
    return render_template('autores/listar.html', autores=autores)

# CREATE - Mostrar formulario de creación
@autores_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        try:
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            nacionalidad = request.form.get('nacionalidad', '').strip()
            
            # Validaciones
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html')
            
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html')
            
            # Convertir fecha de string a date
            fecha_nac_str = request.form.get('fecha_nacimiento')
            fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
            
            # Crear autor
            nuevo_id = get_next_id()
            
            nuevo_autor = Autores(
                id_autor=nuevo_id,
                nombres=nombres,
                apellidos=apellidos,
                nacionalidad=nacionalidad,
                fecha_nacimiento=fecha_nacimiento,
                descripcion=request.form.get('descripcion', ''),
                observaciones=request.form.get('observaciones', '')
            )
            
            db.session.add(nuevo_autor)
            db.session.commit()
            
            flash('Autor creado exitosamente.', 'success')
            return redirect(url_for('autores.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear autor: {str(e)}', 'error')
    
    return render_template('autores/form.html', autor=None)

# UPDATE - Mostrar formulario de edición
@autores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    autor = db.session.get(Autores, id)
    if not autor:
        flash('Autor no encontrado.', 'error')
        return redirect(url_for('autores.listar'))
    
    if request.method == 'POST':
        try:
            nombres = request.form.get('nombres', '').strip()
            apellidos = request.form.get('apellidos', '').strip()
            
            # Validaciones
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html', autor=autor)
            
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html', autor=autor)
            
            # Convertir fecha de string a date
            fecha_nac_str = request.form.get('fecha_nacimiento')
            fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
            
            # Actualizar datos
            autor.nombres = nombres
            autor.apellidos = apellidos
            autor.nacionalidad = request.form.get('nacionalidad', '').strip()
            autor.fecha_nacimiento = fecha_nacimiento
            autor.descripcion = request.form.get('descripcion', '')
            autor.observaciones = request.form.get('observaciones', '')
            
            db.session.commit()
            flash('Autor actualizado exitosamente.', 'success')
            return redirect(url_for('autores.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar autor: {str(e)}', 'error')
    
    return render_template('autores/form.html', autor=autor)

# DELETE - Eliminar autor
@autores_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        autor = db.session.get(Autores, id)
        if not autor:
            flash('Autor no encontrado.', 'error')
            return redirect(url_for('autores.listar'))
        
        db.session.delete(autor)
        db.session.commit()
        flash('Autor eliminado exitosamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar autor: {str(e)}', 'error')
    
    return redirect(url_for('autores.listar'))