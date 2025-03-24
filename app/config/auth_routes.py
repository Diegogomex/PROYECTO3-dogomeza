from flask import Blueprint, request, jsonify, redirect, url_for
from app.models.usuario import Usuario
from flask_login import login_user, logout_user, current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    nombre = data.get("nombre")
    password = data.get("password")

    if not nombre or not password:
        return jsonify({"error": "Nombre de usuario y contraseña son requeridos"}), 400

    usuario = Usuario.query.filter_by(nombre=nombre).first()
    if not usuario or not usuario.verificar_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    login_user(usuario)
    return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario": usuario.nombre}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"mensaje": "Sesión cerrada"}), 200