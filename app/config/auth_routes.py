from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from flask_login import login_user, logout_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Nombre de usuario y contraseña son requeridos"}), 400

    usuario = Usuario.query.filter_by(username=username).first()
    if not usuario or not usuario.verificar_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    login_user(usuario)
    return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario": usuario.username}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"mensaje": "Sesión cerrada"}), 200