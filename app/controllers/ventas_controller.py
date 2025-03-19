from flask import Blueprint

def crear_bp_ventas(heladeria_controller):
    ventas_bp = Blueprint("venta", __name__)

    @ventas_bp.route("/vender/<nombre_producto>")
    def vender_producto(nombre_producto: str):
        try:
            mensaje = heladeria_controller.vender_producto(nombre_producto)
            return mensaje
        except ValueError as e:
            return f"¡Oh no! Nos hemos quedado sin ingredientes: {str(e)}", 400

    return ventas_bp