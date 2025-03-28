from flask import Flask
from app.config.config import Config
from app.config.routes import register_routes
from app.config.db import db, init_db
from app.config.user_data import crear_usuarios_predeterminados
from app.controllers.heladeria_controller import HeladeriaController
from app.controllers.ventas_controller import crear_bp_ventas
from app.config.auth import login_manager
from app.models.usuario import Usuario

def create_app():
    app = Flask(__name__, template_folder="views")
    app.config.from_object(Config)
    
    init_db(app)
    login_manager.init_app(app)
    login_manager.login_view ="home.login"

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        crear_usuarios_predeterminados()

    heladeria_controller = HeladeriaController(app, db) # Crear una instancia del controlador y pasarle app y db
    app.heladeria_controller = heladeria_controller 
    
    ventas_bp = crear_bp_ventas(heladeria_controller)
    app.register_blueprint(ventas_bp)

   
    register_routes(app)
    
    return app

# Cargar usuarios para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))