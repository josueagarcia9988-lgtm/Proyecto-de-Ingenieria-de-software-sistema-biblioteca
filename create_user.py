from app import create_app, db
from models import Clientes
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    # Datos del usuario de prueba
    nuevo_cliente = Clientes(
        nombres="Admin2",
        apellidos="Test",
        email="admin2@test.com",
        password_hash=generate_password_hash("admin123"),
        telefono="12345678",
        direccion="Dirección de prueba",
        tipo_usuario="admin",
        fecha_registro=datetime.now(),
        activo=1,
        ot=0,
        observaciones="Usuario de prueba"
    )
    
    db.session.add(nuevo_cliente)
    db.session.commit()
    
    print("✅ Usuario creado exitosamente!")
    print(f"Email: admin@test.com")
    print(f"Contraseña: admin123")