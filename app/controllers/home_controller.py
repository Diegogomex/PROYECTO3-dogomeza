from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app.models.producto import Producto

home_blueprint = Blueprint("home", __name__)

# Ruta para iniciar sesión
@home_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"Intento de inicio de sesión: username={username}, password={password}")
        user = Usuario.query.filter_by(username=username).first()
        print(f"Usuario encontrado: {user}")  

        if user and user.verificar_password(password):
            login_user(user)  # Iniciar sesión con Flask-Login
            flash("Bienvenido, {}!".format(user.username), "success")
            return redirect(url_for("home.dashboard"))
        else:
            flash("Credenciales incorrectas. Inténtalo de nuevo.", "danger")
    return render_template("login.html")

    # Ruta para cerrar sesión
@home_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()  # Cerrar sesión con Flask-Login
    flash("Sesión cerrada exitosamente.", "info")
    return redirect(url_for("home.index"))

@home_blueprint.route("/")
def index():
    """Página inicial."""
    productos = Producto.query.all()
    return render_template("index.html", productos=productos)

@home_blueprint.route("/dashboard")
@login_required
def dashboard():
    """Dashboard del usuario."""
    productos = Producto.query.all()
    return render_template("dashboard.html", productos=productos, current_user=current_user)