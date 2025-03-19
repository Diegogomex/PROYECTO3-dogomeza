from flask import Flask, render_template
from app.config.config import Config
from app.config.routes import register_routes
from app.config.db import db
from app.config.auth import login_manager
from app.controllers.heladeria_controller import HeladeriaController
from app.models.usuario import Usuario
from app.controllers.ventas_controller import crear_bp_ventas

def create_app():
    app = Flask(__name__, template_folder="views")
    app.config.from_object(Config)
    login_manager.init_app(app)
    login_manager.login_view ="home.login"

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    heladeria_controller = HeladeriaController(app, db) # Crear una instancia del controlador y pasarle app y db
    ventas_bp =crear_bp_ventas (heladeria_controller)
    app.register_blueprint(ventas_bp)
    
    register_routes(app)
    

    @app.route("/")
    def home():
        with app.app_context():
            productos = heladeria_controller.listar_productos()
            return render_template("index.html", productos=productos)
    
    return app

# Cargar usuarios para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))