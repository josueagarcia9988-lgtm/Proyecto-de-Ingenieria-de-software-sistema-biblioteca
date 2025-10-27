from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from models import Autores
from datetime import datetime, date
from sqlalchemy import func
import re

autores_bp = Blueprint('autores', __name__, url_prefix='/autores')

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

def validar_fecha_nacimiento(fecha_str):
    """Validar fecha de nacimiento"""
    if not fecha_str:
        return False, 'Fecha de nacimiento es obligatoria'
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # No puede ser fecha futura
        if fecha > date.today():
            return False, 'La fecha de nacimiento no puede ser futura'
        
        # No puede ser muy antigua (más de 150 años)
        edad_maxima = date.today().year - 150
        if fecha.year < edad_maxima:
            return False, 'Fecha de nacimiento inválida (muy antigua)'
        
        return True, None
    except ValueError:
        return False, 'Formato de fecha inválido'

def validar_nacionalidad(nacionalidad):
    """Validar nacionalidad"""
    if not nacionalidad or not nacionalidad.strip():
        return False, 'Nacionalidad es obligatoria'
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nacionalidad):
        return False, 'Nacionalidad solo puede contener letras'
    if len(nacionalidad.strip()) < 3:
        return False, 'Nacionalidad debe tener al menos 3 caracteres'
    if len(nacionalidad.strip()) > 50:
        return False, 'Nacionalidad no puede exceder 50 caracteres'
    return True, None

def get_next_id():
    """Obtener el siguiente ID disponible para autores"""
    ultimo_id = db.session.query(func.max(Autores.id_autor)).scalar()
    return (ultimo_id or 0) + 1

# READ - Listar todos los autores
@autores_bp.route('/')
@login_required
def listar():
    autores = db.session.query(Autores).order_by(Autores.apellidos, Autores.nombres).all()
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
            fecha_nac_str = request.form.get('fecha_nacimiento', '').strip()
            
            # Validar nombres
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html')
            
            # Validar apellidos
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html')
            
            # Validar nacionalidad
            valido, error = validar_nacionalidad(nacionalidad)
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html')
            
            # Validar fecha de nacimiento
            valido, error = validar_fecha_nacimiento(fecha_nac_str)
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html')
            
            # Verificar si ya existe un autor con el mismo nombre
            autor_existe = db.session.query(Autores).filter(
                func.lower(Autores.nombres) == nombres.lower(),
                func.lower(Autores.apellidos) == apellidos.lower()
            ).first()
            if autor_existe:
                flash(f'Ya existe un autor con el nombre {nombres} {apellidos}.', 'error')
                return render_template('autores/form.html')
            
            # Convertir fecha
            fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
            
            # Crear autor
            nuevo_id = get_next_id()
            
            nuevo_autor = Autores(
                id_autor=nuevo_id,
                nombres=nombres.title(),
                apellidos=apellidos.title(),
                nacionalidad=nacionalidad.title(),
                fecha_nacimiento=fecha_nacimiento,
                descripcion=request.form.get('descripcion', '').strip() or None,
                observaciones=request.form.get('observaciones', '').strip() or None
            )
            
            db.session.add(nuevo_autor)
            db.session.commit()
            
            flash(f'Autor {nombres} {apellidos} creado exitosamente.', 'success')
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
            nacionalidad = request.form.get('nacionalidad', '').strip()
            fecha_nac_str = request.form.get('fecha_nacimiento', '').strip()
            
            # Validar nombres
            valido, error = validar_solo_letras(nombres, 'Nombres')
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html', autor=autor)
            
            # Validar apellidos
            valido, error = validar_solo_letras(apellidos, 'Apellidos')
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html', autor=autor)
            
            # Validar nacionalidad
            valido, error = validar_nacionalidad(nacionalidad)
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html', autor=autor)
            
            # Validar fecha de nacimiento
            valido, error = validar_fecha_nacimiento(fecha_nac_str)
            if not valido:
                flash(error, 'error')
                return render_template('autores/form.html', autor=autor)
            
            # Verificar si ya existe otro autor con el mismo nombre
            autor_existe = db.session.query(Autores).filter(
                func.lower(Autores.nombres) == nombres.lower(),
                func.lower(Autores.apellidos) == apellidos.lower(),
                Autores.id_autor != id
            ).first()
            if autor_existe:
                flash(f'Ya existe otro autor con el nombre {nombres} {apellidos}.', 'error')
                return render_template('autores/form.html', autor=autor)
            
            # Convertir fecha
            fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
            
            # Actualizar datos
            autor.nombres = nombres.title()
            autor.apellidos = apellidos.title()
            autor.nacionalidad = nacionalidad.title()
            autor.fecha_nacimiento = fecha_nacimiento
            autor.descripcion = request.form.get('descripcion', '').strip() or None
            autor.observaciones = request.form.get('observaciones', '').strip() or None
            
            db.session.commit()
            flash(f'Autor {nombres} {apellidos} actualizado exitosamente.', 'success')
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
        
        # Verificar si tiene libros asociados
        if hasattr(autor, 'libros') and autor.libros:
            flash(f'No se puede eliminar a {autor.nombres} {autor.apellidos} porque tiene libros asociados.', 'error')
            return redirect(url_for('autores.listar'))
        
        nombre_completo = f'{autor.nombres} {autor.apellidos}'
        db.session.delete(autor)
        db.session.commit()
        flash(f'Autor {nombre_completo} eliminado exitosamente.', 'error')  # Red notification
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar autor: {str(e)}', 'error')
    
    return redirect(url_for('autores.listar'))