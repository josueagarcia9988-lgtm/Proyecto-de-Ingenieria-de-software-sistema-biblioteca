from typing import Any, Optional
import datetime
import decimal

from sqlalchemy import Boolean, DECIMAL, Date, DateTime, ForeignKeyConstraint, Identity, Index, Integer, LargeBinary, PrimaryKeyConstraint, String, TEXT, Unicode
from sqlalchemy.dialects.mssql import MONEY, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Autores(Base):
    __tablename__ = 'Autores'
    __table_args__ = (
        PrimaryKeyConstraint('id_autor', name='PK_Autor'),
    )

    id_autor: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombres: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    nacionalidad: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_nacimiento: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))
    observaciones: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Libro_Autores: Mapped[list['LibroAutores']] = relationship('LibroAutores', back_populates='Autores_')


class Categorias(Base):
    __tablename__ = 'Categorias'
    __table_args__ = (
        PrimaryKeyConstraint('id_categoria', name='PK_Categorias'),
    )

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    descripcion: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Libro_Categoria: Mapped[list['LibroCategoria']] = relationship('LibroCategoria', back_populates='Categorias_')


class Clientes(Base):
    __tablename__ = 'Clientes'
    __table_args__ = (
        PrimaryKeyConstraint('id_cliente', name='PK_Usuarios'),

        
    )

    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombres: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    email: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255, 'Modern_Spanish_CI_AS'), nullable=False)
    telefono: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    direccion: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    tipo_usuario: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_registro: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    activo: Mapped[int] = mapped_column(TINYINT, nullable=False)
    ot: Mapped[int] = mapped_column(TINYINT, nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Clientes_Documento: Mapped[list['ClientesDocumento']] = relationship('ClientesDocumento', back_populates='Clientes_')
    Notificaciones: Mapped[list['Notificaciones']] = relationship('Notificaciones', back_populates='Clientes_')
    Resenas: Mapped[list['Resenas']] = relationship('Resenas', back_populates='Clientes_')
    Temas_Foros: Mapped[list['TemasForos']] = relationship('TemasForos', back_populates='Clientes_')
    Mensajes_Foros: Mapped[list['MensajesForos']] = relationship('MensajesForos', back_populates='Clientes_')
    Prestamos: Mapped[list['Prestamos']] = relationship('Prestamos', back_populates='Clientes_')
    Tickets: Mapped[list['Tickets']] = relationship('Tickets', back_populates='Clientes_')
    Venta: Mapped[list['Venta']] = relationship('Venta', back_populates='Clientes_')
    Respuesta_Ticket: Mapped[list['RespuestaTicket']] = relationship('RespuestaTicket', back_populates='Clientes_')

    # Métodos requeridos por Flask-Login
    def get_id(self):
        return str(self.id_cliente)
    
    @property
    def is_active(self):
        return bool(self.activo)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False


class EstadoVenta(Base):
    __tablename__ = 'Estado_Venta'
    __table_args__ = (
        PrimaryKeyConstraint('id_estado', name='PK_Estado'),
    )

    id_estado: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    descripcion: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    activo: Mapped[int] = mapped_column(TINYINT, nullable=False)

    Venta: Mapped[list['Venta']] = relationship('Venta', back_populates='Estado_Venta')


class Libros(Base):
    __tablename__ = 'Libros'
    __table_args__ = (
        PrimaryKeyConstraint('id_libro', name='PK_Libros'),
    )

    id_libro: Mapped[int] = mapped_column(Integer, primary_key=True)
    isbn: Mapped[str] = mapped_column(String(13, 'Modern_Spanish_CI_AS'), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255, 'Modern_Spanish_CI_AS'), nullable=False)
    formato: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    num_pag: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_fisico: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_digital: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_venta: Mapped[Any] = mapped_column(MONEY, nullable=False)
    precio_prestamo: Mapped[Any] = mapped_column(MONEY, nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))
    descripcion: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))
    portada: Mapped[Optional[str]] = mapped_column(String(255, 'Modern_Spanish_CI_AS'))
    disp_venta: Mapped[Optional[int]] = mapped_column(TINYINT)
    disp_prestamo: Mapped[Optional[int]] = mapped_column(TINYINT)

    Inventarios: Mapped[list['Inventarios']] = relationship('Inventarios', back_populates='Libros_')
    Libro_Autores: Mapped[list['LibroAutores']] = relationship('LibroAutores', back_populates='Libros_')
    Libro_Categoria: Mapped[list['LibroCategoria']] = relationship('LibroCategoria', back_populates='Libros_')
    Resenas: Mapped[list['Resenas']] = relationship('Resenas', back_populates='Libros_')
    Libro_Editoriales: Mapped[list['LibroEditoriales']] = relationship('LibroEditoriales', back_populates='Libros_')
    Detalle_Venta: Mapped[list['DetalleVenta']] = relationship('DetalleVenta', back_populates='Libros_')
    Detalles_Prestamos: Mapped[list['DetallesPrestamos']] = relationship('DetallesPrestamos', back_populates='Libros_')


class MetodoDePago(Base):
    __tablename__ = 'Metodo_De_Pago'
    __table_args__ = (
        PrimaryKeyConstraint('id_metodo_pago', name='PK_Metodo_De_Pago'),
    )

    id_metodo_pago: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    descripcion: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    activo: Mapped[int] = mapped_column(TINYINT, nullable=False)

    Venta: Mapped[list['Venta']] = relationship('Venta', back_populates='Metodo_De_Pago')


class Pais(Base):
    __tablename__ = 'Pais'
    __table_args__ = (
        PrimaryKeyConstraint('id_pais', name='PK_Pais'),
    )

    id_pais: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_pais: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    codigo_iso: Mapped[str] = mapped_column(String(5, 'Modern_Spanish_CI_AS'), nullable=False)

    Editoriales: Mapped[list['Editoriales']] = relationship('Editoriales', back_populates='Pais_')
    Empleados: Mapped[list['Empleados']] = relationship('Empleados', back_populates='Pais_')


class Sucursales(Base):
    __tablename__ = 'Sucursales'
    __table_args__ = (
        PrimaryKeyConstraint('id_sucursal', name='PK_Sucursales'),
    )

    id_sucursal: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    direccion: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20, 'Modern_Spanish_CI_AS'), nullable=False)
    email: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    departamento: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    codigo_postal: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    activo: Mapped[int] = mapped_column(TINYINT, nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Empleados: Mapped[list['Empleados']] = relationship('Empleados', back_populates='Sucursales_')
    Inventarios: Mapped[list['Inventarios']] = relationship('Inventarios', back_populates='Sucursales_')
    Facturas_Sar: Mapped[list['FacturasSar']] = relationship('FacturasSar', back_populates='Sucursales_')


class TiposDocumentos(Base):
    __tablename__ = 'Tipos_Documentos'
    __table_args__ = (
        PrimaryKeyConstraint('id_tipo_documento', name='PK_Tipos_Documentos'),
    )

    id_tipo_documento: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(Unicode(50, 'Modern_Spanish_CI_AS'), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Unicode(150, 'Modern_Spanish_CI_AS'))

    Clientes_Documento: Mapped[list['ClientesDocumento']] = relationship('ClientesDocumento', back_populates='Tipos_Documentos')
    Empleados_Documento: Mapped[list['EmpleadosDocumento']] = relationship('EmpleadosDocumento', back_populates='Tipos_Documentos')


class Sysdiagrams(Base):
    __tablename__ = 'sysdiagrams'
    __table_args__ = (
        PrimaryKeyConstraint('diagram_id', name='PK__sysdiagr__C2B05B6138CD444C'),
        Index('UK_principal_name', 'principal_id', 'name', unique=True)
    )

    name: Mapped[str] = mapped_column(Unicode(128, 'Modern_Spanish_CI_AS'), nullable=False)
    principal_id: Mapped[int] = mapped_column(Integer, nullable=False)
    diagram_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    version: Mapped[Optional[int]] = mapped_column(Integer)
    definition: Mapped[Optional[bytes]] = mapped_column(LargeBinary)


class ClientesDocumento(Base):
    __tablename__ = 'Clientes_Documento'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Clientes.id_cliente'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Clientes_Documento_Clientes'),
        ForeignKeyConstraint(['id_tipo_documento'], ['Tipos_Documentos.id_tipo_documento'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Clientes_Documento_Tipos_Documentos'),
        PrimaryKeyConstraint('id_cliente_documento', name='PK_Clientes_Documento'),
        Index('IXFK_Clientes_Documento_Clientes', 'id_cliente'),
        Index('IXFK_Clientes_Documento_Tipos_Documentos', 'id_tipo_documento')
    )

    id_cliente_documento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_tipo_documento: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_documento: Mapped[str] = mapped_column(Unicode(50, 'Modern_Spanish_CI_AS'), nullable=False)

    Clientes_: Mapped['Clientes'] = relationship('Clientes', back_populates='Clientes_Documento')
    Tipos_Documentos: Mapped['TiposDocumentos'] = relationship('TiposDocumentos', back_populates='Clientes_Documento')


class Editoriales(Base):
    __tablename__ = 'Editoriales'
    __table_args__ = (
        ForeignKeyConstraint(['id_pais'], ['Pais.id_pais'], name='FK_Editoriales_Pais'),
        PrimaryKeyConstraint('id_editorial', name='PK_Editorial'),
        Index('IXFK_Editoriales_Pais', 'id_pais')
    )

    id_editorial: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150, 'Modern_Spanish_CI_AS'), nullable=False)
    id_pais: Mapped[int] = mapped_column(Integer, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20, 'Modern_Spanish_CI_AS'), nullable=False)
    email: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(200, 'Modern_Spanish_CI_AS'))

    Pais_: Mapped['Pais'] = relationship('Pais', back_populates='Editoriales')
    Libro_Editoriales: Mapped[list['LibroEditoriales']] = relationship('LibroEditoriales', back_populates='Editoriales_')


class Empleados(Base):
    __tablename__ = 'Empleados'
    __table_args__ = (
        ForeignKeyConstraint(['id_pais'], ['Pais.id_pais'], name='FK_Empleados_Pais'),
        ForeignKeyConstraint(['id_sucursal'], ['Sucursales.id_sucursal'], name='FK_Empleados_Sucursales'),
        PrimaryKeyConstraint('id_empleado', name='PK_Empleados'),
        Index('IXFK_Empleados_Pais', 'id_pais'),
        Index('IXFK_Empleados_Sucursales', 'id_sucursal')
    )

    id_empleado: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_sucursal: Mapped[int] = mapped_column(Integer, nullable=False)
    id_pais: Mapped[int] = mapped_column(Integer, nullable=False)
    nombres: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    usuario: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    email: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255, 'Modern_Spanish_CI_AS'), nullable=False)
    telefono: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    rol: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_contratacion: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    salario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    activo: Mapped[int] = mapped_column(TINYINT, nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Pais_: Mapped['Pais'] = relationship('Pais', back_populates='Empleados')
    Sucursales_: Mapped['Sucursales'] = relationship('Sucursales', back_populates='Empleados')
    Empleados_Documento: Mapped[list['EmpleadosDocumento']] = relationship('EmpleadosDocumento', back_populates='Empleados_')
    Prestamos: Mapped[list['Prestamos']] = relationship('Prestamos', back_populates='Empleados_')
    Tickets: Mapped[list['Tickets']] = relationship('Tickets', back_populates='Empleados_')
    Venta: Mapped[list['Venta']] = relationship('Venta', back_populates='Empleados_')
    Respuesta_Ticket: Mapped[list['RespuestaTicket']] = relationship('RespuestaTicket', back_populates='Empleados_')


class Inventarios(Base):
    __tablename__ = 'Inventarios'
    __table_args__ = (
        ForeignKeyConstraint(['id_libro'], ['Libros.id_libro'], name='FK_Inventarios_Libros'),
        ForeignKeyConstraint(['id_sucursal'], ['Sucursales.id_sucursal'], name='FK_Inventarios_Sucursales'),
        PrimaryKeyConstraint('id_inventario', name='PK_Inventarios'),
        Index('IXFK_Inventarios_Libros', 'id_libro'),
        Index('IXFK_Inventarios_Sucursales', 'id_sucursal')
    )

    id_inventario: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_libro: Mapped[int] = mapped_column(Integer, nullable=False)
    id_sucursal: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_movimiento: Mapped[str] = mapped_column(String(200, 'Modern_Spanish_CI_AS'), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_anterior: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_nuevo: Mapped[int] = mapped_column(Integer, nullable=False)
    formato: Mapped[str] = mapped_column(String(200, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_movimiento: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))
    referencia: Mapped[Optional[str]] = mapped_column(String(100, 'Modern_Spanish_CI_AS'))

    Libros_: Mapped['Libros'] = relationship('Libros', back_populates='Inventarios')
    Sucursales_: Mapped['Sucursales'] = relationship('Sucursales', back_populates='Inventarios')


class LibroAutores(Base):
    __tablename__ = 'Libro_Autores'
    __table_args__ = (
        ForeignKeyConstraint(['id_autor'], ['Autores.id_autor'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Libro_Autor_Autor'),
        ForeignKeyConstraint(['id_libro'], ['Libros.id_libro'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Libro_Autor_Libros'),
        PrimaryKeyConstraint('id_libro_autor', name='PK_Libro_Autor'),
        Index('IXFK_Libro_Autor_Autor', 'id_autor'),
        Index('IXFK_Libro_Autor_Libros', 'id_libro')
    )

    id_libro_autor: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_libro: Mapped[int] = mapped_column(Integer, nullable=False)
    id_autor: Mapped[int] = mapped_column(Integer, nullable=False)

    Autores_: Mapped['Autores'] = relationship('Autores', back_populates='Libro_Autores')
    Libros_: Mapped['Libros'] = relationship('Libros', back_populates='Libro_Autores')


class LibroCategoria(Base):
    __tablename__ = 'Libro_Categoria'
    __table_args__ = (
        ForeignKeyConstraint(['id_categoria'], ['Categorias.id_categoria'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Libro_Categoria_Categorias'),
        ForeignKeyConstraint(['id_libro'], ['Libros.id_libro'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Libro_Categoria_Libros'),
        PrimaryKeyConstraint('id_libro_categoria', name='PK_Libro_Categoria'),
        Index('IXFK_Libro_Categoria_Categorias', 'id_categoria'),
        Index('IXFK_Libro_Categoria_Libros', 'id_libro')
    )

    id_libro_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_categoria: Mapped[int] = mapped_column(Integer, nullable=False)
    id_libro: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Categorias_: Mapped['Categorias'] = relationship('Categorias', back_populates='Libro_Categoria')
    Libros_: Mapped['Libros'] = relationship('Libros', back_populates='Libro_Categoria')


class Notificaciones(Base):
    __tablename__ = 'Notificaciones'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Clientes.id_cliente'], name='FK_Notificaciones_Clientes'),
        PrimaryKeyConstraint('id_notificacion', name='PK_Notificaciones'),
        Index('IXFK_Notificaciones_Clientes', 'id_cliente')
    )

    id_notificacion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    titulo: Mapped[str] = mapped_column(String(200, 'Modern_Spanish_CI_AS'), nullable=False)
    mensaje: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    tipo: Mapped[str] = mapped_column(Unicode(200, 'Modern_Spanish_CI_AS'), nullable=False)
    leido: Mapped[bool] = mapped_column(Boolean, nullable=False)
    fecha_envio: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    Clientes_: Mapped['Clientes'] = relationship('Clientes', back_populates='Notificaciones')


class Resenas(Base):
    __tablename__ = 'Resenas'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Clientes.id_cliente'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Resenas_Clientes'),
        ForeignKeyConstraint(['id_libro'], ['Libros.id_libro'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Resenas_Libros'),
        PrimaryKeyConstraint('id_resena', name='PK_Resenas'),
        Index('IXFK_Resenas_Clientes', 'id_cliente'),
        Index('IXFK_Resenas_Libros', 'id_libro')
    )

    id_resena: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_libro: Mapped[int] = mapped_column(Integer, nullable=False)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    calificacion: Mapped[int] = mapped_column(TINYINT, nullable=False)
    titulo: Mapped[str] = mapped_column(String(200, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_resena: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    visible: Mapped[bool] = mapped_column(Boolean, nullable=False)
    comentario: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Clientes_: Mapped['Clientes'] = relationship('Clientes', back_populates='Resenas')
    Libros_: Mapped['Libros'] = relationship('Libros', back_populates='Resenas')


class TemasForos(Base):
    __tablename__ = 'Temas_Foros'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente_creador'], ['Clientes.id_cliente'], name='FK_Temas_Foros_Clientes'),
        PrimaryKeyConstraint('id_tema', name='PK_Temas_Foros'),
        Index('IXFK_Temas_Foros_Clientes', 'id_cliente_creador')
    )

    id_tema: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente_creador: Mapped[int] = mapped_column(Integer, nullable=False)
    categoria_foro: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    activo: Mapped[int] = mapped_column(TINYINT, nullable=False)
    destacado: Mapped[int] = mapped_column(TINYINT, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))
    vistas: Mapped[Optional[int]] = mapped_column(Integer)

    Clientes_: Mapped['Clientes'] = relationship('Clientes', back_populates='Temas_Foros')
    Mensajes_Foros: Mapped[list['MensajesForos']] = relationship('MensajesForos', back_populates='Temas_Foros')


class EmpleadosDocumento(Base):
    __tablename__ = 'Empleados_Documento'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['Empleados.id_empleado'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Empleados_Documento_Empleados'),
        ForeignKeyConstraint(['id_tipo_documento'], ['Tipos_Documentos.id_tipo_documento'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Empleados_Documento_Tipos_Documentos'),
        PrimaryKeyConstraint('id_empleado_documento', name='PK_Empleados_Documento'),
        Index('IXFK_Empleados_Documento_Empleados', 'id_empleado'),
        Index('IXFK_Empleados_Documento_Tipos_Documentos', 'id_tipo_documento')
    )

    id_empleado_documento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_tipo_documento: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_documento: Mapped[str] = mapped_column(Unicode(50, 'Modern_Spanish_CI_AS'), nullable=False)

    Empleados_: Mapped['Empleados'] = relationship('Empleados', back_populates='Empleados_Documento')
    Tipos_Documentos: Mapped['TiposDocumentos'] = relationship('TiposDocumentos', back_populates='Empleados_Documento')


class LibroEditoriales(Base):
    __tablename__ = 'Libro_Editoriales'
    __table_args__ = (
        ForeignKeyConstraint(['id_editorial'], ['Editoriales.id_editorial'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Libro_Editoriales_Editoriales'),
        ForeignKeyConstraint(['id_libro'], ['Libros.id_libro'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Libro_Editoriales_Libros'),
        PrimaryKeyConstraint('id_libros_editoriales', name='PK_Libro_Editoriales'),
        Index('IXFK_Libro_Editoriales_Editoriales', 'id_editorial'),
        Index('IXFK_Libro_Editoriales_Libros', 'id_libro')
    )

    id_libros_editoriales: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_editorial: Mapped[int] = mapped_column(Integer, nullable=False)
    id_libro: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Editoriales_: Mapped['Editoriales'] = relationship('Editoriales', back_populates='Libro_Editoriales')
    Libros_: Mapped['Libros'] = relationship('Libros', back_populates='Libro_Editoriales')


class MensajesForos(Base):
    __tablename__ = 'Mensajes_Foros'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Clientes.id_cliente'], name='FK_Mensajes_Foros_Clientes'),
        ForeignKeyConstraint(['id_mensaje_padre'], ['Mensajes_Foros.id_mensaje'], name='FK_Mensaje_Foro_Mensaje_Foro'),
        ForeignKeyConstraint(['id_tema'], ['Temas_Foros.id_tema'], name='FK_Mensajes_Foros_Temas'),
        PrimaryKeyConstraint('id_mensaje', name='PK_Mensaje_Foro'),
        Index('IXFK_Mensaje_Foro_Mensaje_Foro', 'id_mensaje_padre'),
        Index('IXFK_Mensajes_Foros_Clientes', 'id_cliente'),
        Index('IXFK_Mensajes_Foros_Temas', 'id_tema')
    )

    id_mensaje: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_tema: Mapped[int] = mapped_column(Integer, nullable=False)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    contenido: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_publicacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    visible: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_mensaje_padre: Mapped[Optional[int]] = mapped_column(Integer)
    fecha_edicion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    Clientes_: Mapped['Clientes'] = relationship('Clientes', back_populates='Mensajes_Foros')
    Mensajes_Foros: Mapped[Optional['MensajesForos']] = relationship('MensajesForos', remote_side=[id_mensaje], back_populates='Mensajes_Foros_reverse')
    Mensajes_Foros_reverse: Mapped[list['MensajesForos']] = relationship('MensajesForos', remote_side=[id_mensaje_padre], back_populates='Mensajes_Foros')
    Temas_Foros: Mapped['TemasForos'] = relationship('TemasForos', back_populates='Mensajes_Foros')


class Prestamos(Base):
    __tablename__ = 'Prestamos'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Clientes.id_cliente'], name='FK_Prestamos_Clientes'),
        ForeignKeyConstraint(['id_empleado'], ['Empleados.id_empleado'], name='FK_Prestamos_Empleados'),
        PrimaryKeyConstraint('id_prestamo', name='PK_Prestamos'),
        Index('IXFK_Prestamos_Clientes', 'id_cliente'),
        Index('IXFK_Prestamos_Empleados', 'id_empleado')
    )

    id_prestamo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_prestamo: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_devolucion_estimada: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(200, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_devolucion_real: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    observaciones: Mapped[Optional[str]] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'))

    Clientes_: Mapped['Clientes'] = relationship('Clientes', back_populates='Prestamos')
    Empleados_: Mapped['Empleados'] = relationship('Empleados', back_populates='Prestamos')
    Detalles_Prestamos: Mapped[list['DetallesPrestamos']] = relationship('DetallesPrestamos', back_populates='Prestamos_')


class Tickets(Base):
    __tablename__ = 'Tickets'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Clientes.id_cliente'], name='FK_Tickets_Clientes'),
        ForeignKeyConstraint(['id_empleado_asignado'], ['Empleados.id_empleado'], name='FK_Tickets_Empleados'),
        PrimaryKeyConstraint('id_ticket', name='PK_tickets'),
        Index('IXFK_Tickets_Clientes', 'id_cliente'),
        Index('IXFK_Tickets_Empleados', 'id_empleado_asignado')
    )

    id_ticket: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    asunto: Mapped[str] = mapped_column(String(100, 'Modern_Spanish_CI_AS'), nullable=False)
    descripcion: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    prioridad: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    estado: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    id_empleado_asignado: Mapped[Optional[int]] = mapped_column(Integer)
    fecha_actualizacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fecha_cierre: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    Clientes_: Mapped['Clientes'] = relationship('Clientes', back_populates='Tickets')
    Empleados_: Mapped[Optional['Empleados']] = relationship('Empleados', back_populates='Tickets')
    Respuesta_Ticket: Mapped[list['RespuestaTicket']] = relationship('RespuestaTicket', back_populates='Tickets_')


class Venta(Base):
    __tablename__ = 'Venta'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Clientes.id_cliente'], name='FK_Venta_Clientes'),
        ForeignKeyConstraint(['id_empleado'], ['Empleados.id_empleado'], name='FK_Venta_Empleados'),
        ForeignKeyConstraint(['id_estado'], ['Estado_Venta.id_estado'], name='FK_Venta_Estado_Venta'),
        ForeignKeyConstraint(['id_metodo_pago'], ['Metodo_De_Pago.id_metodo_pago'], name='FK_Venta_Metodo_De_Pago'),
        PrimaryKeyConstraint('id_venta', name='PK_Venta'),
        Index('IXFK_Venta_Clientes', 'id_cliente'),
        Index('IXFK_Venta_Empleados', 'id_empleado'),
        Index('IXFK_Venta_Estado_Venta', 'id_estado'),
        Index('IXFK_Venta_Metodo_De_Pago', 'id_metodo_pago')
    )

    id_venta: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_metodo_pago: Mapped[int] = mapped_column(Integer, nullable=False)
    id_estado: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_venta: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    isv_15: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    isv_18: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    descuento: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    exonerado: Mapped[int] = mapped_column(TINYINT, nullable=False)
    numero_factura: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    importe_exonerado: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    numero_reg_exoneracion: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    numero_reg_sag: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)

    Clientes_: Mapped['Clientes'] = relationship('Clientes', back_populates='Venta')
    Empleados_: Mapped['Empleados'] = relationship('Empleados', back_populates='Venta')
    Estado_Venta: Mapped['EstadoVenta'] = relationship('EstadoVenta', back_populates='Venta')
    Metodo_De_Pago: Mapped['MetodoDePago'] = relationship('MetodoDePago', back_populates='Venta')
    Detalle_Venta: Mapped[list['DetalleVenta']] = relationship('DetalleVenta', back_populates='Venta_')
    Facturas_Sar: Mapped[list['FacturasSar']] = relationship('FacturasSar', back_populates='Venta_')


class DetalleVenta(Base):
    __tablename__ = 'Detalle_Venta'
    __table_args__ = (
        ForeignKeyConstraint(['id_libro'], ['Libros.id_libro'], name='FK_Detalle_Venta_Libros'),
        ForeignKeyConstraint(['id_venta'], ['Venta.id_venta'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Detalle_Venta_Venta'),
        PrimaryKeyConstraint('id_detalle', name='PK_Detalle_Venta'),
        Index('IXFK_Detalle_Venta_Libros', 'id_libro'),
        Index('IXFK_Detalle_Venta_Venta', 'id_venta')
    )

    id_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_venta: Mapped[int] = mapped_column(Integer, nullable=False)
    id_libro: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    Libros_: Mapped['Libros'] = relationship('Libros', back_populates='Detalle_Venta')
    Venta_: Mapped['Venta'] = relationship('Venta', back_populates='Detalle_Venta')


class DetallesPrestamos(Base):
    __tablename__ = 'Detalles_Prestamos'
    __table_args__ = (
        ForeignKeyConstraint(['id_libro'], ['Libros.id_libro'], name='FK_Detalles_Prestamos_Libros'),
        ForeignKeyConstraint(['id_prestamos'], ['Prestamos.id_prestamo'], ondelete='CASCADE', onupdate='CASCADE', name='FK_Detalles_Prestamos_Prestamos'),
        PrimaryKeyConstraint('id_detalle_prestamos', name='PK_Detalles_Prestamos'),
        Index('IXFK_Detalles_Prestamos_Libros', 'id_libro'),
        Index('IXFK_Detalles_Prestamos_Prestamos', 'id_prestamos')
    )

    id_detalle_prestamos: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_prestamos: Mapped[int] = mapped_column(Integer, nullable=False)
    id_libro: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_prestamo: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_devolucion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    estado: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    multa: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    Libros_: Mapped['Libros'] = relationship('Libros', back_populates='Detalles_Prestamos')
    Prestamos_: Mapped['Prestamos'] = relationship('Prestamos', back_populates='Detalles_Prestamos')


class FacturasSar(Base):
    __tablename__ = 'Facturas_Sar'
    __table_args__ = (
        ForeignKeyConstraint(['id_sucursal'], ['Sucursales.id_sucursal'], name='FK_Facturas_Sar_Sucursales'),
        ForeignKeyConstraint(['id_venta'], ['Venta.id_venta'], onupdate='CASCADE', name='FK_Facturas_Sar_Venta'),
        PrimaryKeyConstraint('id_parametro', name='PK_Factura_Sar'),
        Index('IXFK_Facturas_Sar_Sucursales', 'id_sucursal'),
        Index('IXFK_Facturas_Sar_Venta', 'id_venta')
    )

    id_parametro: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_venta: Mapped[int] = mapped_column(Integer, nullable=False)
    id_sucursal: Mapped[int] = mapped_column(Integer, nullable=False)
    cai: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    rango_inicial: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    fecha_emision: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    rango_final: Mapped[str] = mapped_column(String(50, 'Modern_Spanish_CI_AS'), nullable=False)
    rtn_empresa: Mapped[str] = mapped_column(String(20, 'Modern_Spanish_CI_AS'), nullable=False)
    anulada: Mapped[int] = mapped_column(TINYINT, nullable=False)
    fecha_anulacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ultima_factura: Mapped[Optional[str]] = mapped_column(String(50, 'Modern_Spanish_CI_AS'))

    Sucursales_: Mapped['Sucursales'] = relationship('Sucursales', back_populates='Facturas_Sar')
    Venta_: Mapped['Venta'] = relationship('Venta', back_populates='Facturas_Sar')


class RespuestaTicket(Base):
    __tablename__ = 'Respuesta_Ticket'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Clientes.id_cliente'], name='FK_Respuesta_Ticket_Clientes'),
        ForeignKeyConstraint(['id_empleado'], ['Empleados.id_empleado'], name='FK_Respuesta_Ticket_Empleados'),
        ForeignKeyConstraint(['id_ticket'], ['Tickets.id_ticket'], name='FK_Respuesta_Ticket_Tickets'),
        PrimaryKeyConstraint('id_respuesta', name='PK_Respuesta_Ticket'),
        Index('IXFK_Respuesta_Ticket_Clientes', 'id_cliente'),
        Index('IXFK_Respuesta_Ticket_Empleados', 'id_empleado'),
        Index('IXFK_Respuesta_Ticket_Tickets', 'id_ticket')
    )

    id_respuesta: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_ticket: Mapped[int] = mapped_column(Integer, nullable=False)
    mensaje: Mapped[str] = mapped_column(TEXT(2147483647, 'Modern_Spanish_CI_AS'), nullable=False)
    fecha_respuesta: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    es_solucion: Mapped[int] = mapped_column(TINYINT, nullable=False)
    id_cliente: Mapped[Optional[int]] = mapped_column(Integer)
    id_empleado: Mapped[Optional[int]] = mapped_column(Integer)

    Clientes_: Mapped[Optional['Clientes']] = relationship('Clientes', back_populates='Respuesta_Ticket')
    Empleados_: Mapped[Optional['Empleados']] = relationship('Empleados', back_populates='Respuesta_Ticket')
    Tickets_: Mapped['Tickets'] = relationship('Tickets', back_populates='Respuesta_Ticket')
