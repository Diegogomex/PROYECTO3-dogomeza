from flask import render_template
from app import app

@app.errorhandler(401)
def no_autorizado(error):
    """Muestra una página de error para accesos no autorizados."""
    return render_template("errors/401.html"), 401