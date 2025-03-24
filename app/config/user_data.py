from app.models.usuario import Usuario
from app.config.db import db
from werkzeug.security import generate_password_hash

def crear_usuarios_predeterminados():
    """
    Crea usuarios predeterminados si no existen en la base de datos.
    """
    if Usuario.query.count() == 0:
        admin_password = generate_password_hash("admin123", method="pbkdf2:sha256")
        empleado_password = generate_password_hash("empleado123", method="pbkdf2:sha256")
        cliente_password = generate_password_hash("cliente123", method="pbkdf2:sha256")

        print(f"Contraseña Admin: {admin_password}")
        print(f"Contraseña Empleado: {empleado_password}")
        print(f"Contraseña Cliente: {cliente_password}")

        # Crear usuarios predeterminados
        admin = Usuario(
            username="Admin",
            password= admin_password,
            es_admin=True,
            es_empleado=False
        )
        empleado = Usuario(
            password=empleado_password,
            username="Empleado",
            es_admin=False,
            es_empleado=True
        )
        cliente = Usuario(
            username="Cliente",
            password=cliente_password,
            es_admin=False,
            es_empleado=False
        )

        # Agregar usuarios a la base de datos
        db.session.add_all([admin, empleado, cliente])
        db.session.commit()

        admin_db = Usuario.query.filter_by(username="Admin").first()
        print(f"Admin Password (Stored in DB): {admin_db.password}")