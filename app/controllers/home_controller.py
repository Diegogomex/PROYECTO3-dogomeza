from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required 
from app.models.usuario import Usuario
from app.config.auth import login_manager

home_blueprint = Blueprint("home", __name__)

# Ruta para iniciar sesión
@home_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Usuario.query.filter_by(username=username).first()
        if user and user.verificar_password(password):
            login_user(user)  # Iniciar sesión con Flask-Login
            flash("Bienvenido, {}!".format(user.username), "success")
            return redirect(url_for("home.home"))
        else:
            flash("Credenciales incorrectas. Inténtalo de nuevo.", "danger")
    return render_template("login.html")

    # Ruta para cerrar sesión
@home_blueprint.route("/logout")
@login_required
def logout():
    logout_user()  # Cerrar sesión con Flask-Login
    flash("Sesión cerrada exitosamente.", "info")
    return redirect(url_for("home.login"))
