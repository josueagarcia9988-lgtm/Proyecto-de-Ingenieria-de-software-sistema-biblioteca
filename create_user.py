from app import create_app, db
from models import Clientes
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy import func

app = create_app()

with app.app_context():
    # Obtener el último ID y sumar 1
    ultimo_id = db.session.query(func.max(Clientes.id_cliente)).scalar()
    nuevo_id = (ultimo_id or 0) + 1
    
    # Crear usuario admin
    nuevo_admin = Clientes(
        id_cliente=nuevo_id,
        nombres="Admin",
        apellidos="Sistema",
        email="admin@biblioteca.com",
        password_hash=generate_password_hash("admin123"),
        telefono="99999999",
        direccion="Oficina Principal",
        tipo_usuario="admin",  # Usuario administrador
        fecha_registro=datetime.now(),
        activo=1,
        ot=0,
        observaciones="Usuario administrador del sistema"
    )
    
    db.session.add(nuevo_admin)
    db.session.commit()
    
    print("✅ Usuario administrador creado exitosamente!")
    print(f"ID: {nuevo_id}")
    print(f"Email: admin@biblioteca.com")
    print(f"Contraseña: admin123")
    print(f"Tipo: admin")