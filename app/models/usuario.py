from app.config.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = generate_password_hash(password)
        
    def verificar_password(self, password:str)-> bool:
        """
        Verifica si la contraseña proporcionada coincide con la almacenada.
        Parámetros:
        - password (str): Contraseña en texto plano.
        Retorna:
        - bool: True si la contraseña coincide, False si no coincide
        """
        return check_password_hash(self.password, password)
    
    @staticmethod
    def buscar_por_username(username: str):
        """
        Busca un usuario por su nombre de usuario.
        Parámetros:
        - username (str): Nombre de usuario a buscar.
        Retorna:
        - Usuario: Instancia del usuario encontrado, o None si no existe.
        """
        return Usuario.query.filter_by(username=username).first()
    
    def __repr__(self):
        return f"<Usuario {self.username}>"