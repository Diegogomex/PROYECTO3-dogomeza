from app.controllers.home_controller import home_blueprint
from app.controllers.api_controller import api_bp
from app.config.auth_routes import auth_bp

def register_routes(app):
   
    app.register_blueprint(home_blueprint)
    app.register_blueprint(api_bp)         
    app.register_blueprint(auth_bp)         


