from flask import Blueprint, jsonify, request, abort
#from flask_login import login_required, current_user
from app.models.producto import Producto
from app.models.ingrediente import Ingrediente
from app.models. heladeria import Heladeria
from app.config.db import db
from sqlalchemy.orm import joinedload

api_bp = Blueprint("api", __name__, url_prefix="/api")

heladeria = Heladeria("DG Heladería")

def get_heladeria_controller():
    from flask import current_app
    return current_app.heladeria_controller

def get_producto_id(producto_id):
    producto = Producto.query.options(joinedload(Producto.ingredientes)).get(producto_id)
    if not producto:
        abort(404, description="Producto no encontrado")
    return producto

def get_ingrediente_id(ingrediente_id):
    ingrediente = Ingrediente.query.get (ingrediente_id)
    if not ingrediente:
        abort(404, description="Ingrediente no encontrado")
    return ingrediente

#Productos

@api_bp.route("/productos", methods=["GET"])
def listar_productos():
    """Listar todos los productos."""
    productos = Producto.query.all()
    return jsonify([{"id": p.id, "nombre": p.nombre, "precio_publico": p.precio_publico} for p in productos])

@api_bp.route("/productos/<int:producto_id>", methods=["GET"])
def obtener_producto_por_id(producto_id):
    """Obtener un producto por su ID."""
    producto = get_producto_id(producto_id)
    return jsonify({"id": producto.id, "nombre": producto.nombre, "precio_publico": producto.precio_publico})

@api_bp.route("/productos/nombre/<string:nombre>", methods=["GET"])
def obtener_producto_por_nombre(nombre):
    """Obtener un producto por su nombre."""
    producto = Producto.query.filter_by(nombre=nombre).first()
    if not producto:
        abort(404, description="Producto no encontrado")
    return jsonify({"id": producto.id, "nombre": producto.nombre, "precio_publico": producto.precio_publico})

@api_bp.route("/productos/<int:producto_id>/calorias", methods=["GET"])
#@login_required
def obtener_calorias_producto(producto_id):
    """Consultar las calorías de un producto por su ID."""
    #if not current_user.is_authenticated or (not current_user.es_admin and not current_user.es_empleado):
    #    abort (401) #no autorizado
    producto = get_producto_id(producto_id)
    calorias = producto.calcular_calorias()
    return jsonify({"id": producto.id, "nombre": producto.nombre, "calorias": calorias})

@api_bp.route("/productos/<int:producto_id>/rentabilidad", methods=["GET"])
#@login_required
def obtener_rentabilidad_producto(producto_id):
    """Consultar la rentabilidad de un producto por su ID."""
    #if not current_user.is_authenticated or not current_user.es_admin:
    #    abort (401) #no autorizado
    producto = get_producto_id(producto_id)
    rentabilidad = producto.calcular_rentabilidad()
    return jsonify({"id": producto.id, "nombre": producto.nombre, "rentabilidad": rentabilidad})

@api_bp.route("/productos/<int:producto_id>/costo", methods=["GET"])
def obtener_costo_producto(producto_id):
    """Consultar el costo de producción de un producto por su ID."""
    producto = get_producto_id(producto_id)
    costo = producto.calcular_costo()
    return jsonify({"id": producto.id, "nombre": producto.nombre, "costo_produccion": costo})

@api_bp.route("/productos/<int:producto_id>/vender", methods=["POST"])
#@login_required
def vender_producto_api(producto_id):
    """Vender un producto por su ID."""
    #if not current_user.is_authenticated or (not current_user.es_admin and not current_user.es_empleado):
    #    abort (401) #no autorizado
    heladeria_controller = get_heladeria_controller()
    producto = get_producto_id(producto_id)
    try:
        mensaje = heladeria_controller.heladeria.vender(producto, db.session)
        return jsonify({"mensaje": mensaje}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route("/productos/<int:producto_id>/reabastecer", methods=["POST"])
def reabastecer_producto(producto_id):
    """Reabastecer inventario de un producto por su ID."""
    producto = get_producto_id(producto_id)
    try:
        # Obtener la cantidad del cuerpo JSON
        data = request.get_json()  
        if not data or "cantidad" not in data:
            return jsonify({"error": "Debe proporcionar 'cantidad' en el cuerpo JSON."}), 400

        cantidad = data["cantidad"]
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            return jsonify({"error": "'cantidad' debe ser un número positivo."}), 400

        # Reabastecer el inventario
        for ingrediente in producto.ingredientes:
            ingrediente.abastecer(cantidad)

        db.session.commit()
        return jsonify({"mensaje": f"Inventario de {producto.nombre} reabastecido"}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Ingredientes

@api_bp.route("/ingredientes", methods=["GET"])
def listar_ingredientes():
    """Listar todos los ingredientes."""
    ingredientes = Ingrediente.query.all()
    return jsonify([{"id": i.id, "nombre": i.nombre, "inventario": i.inventario} for i in ingredientes])

@api_bp.route("/ingredientes/<int:ingrediente_id>", methods=["GET"])
def obtener_ingrediente_por_id(ingrediente_id):
    """Obtener un ingrediente por su ID."""
    ingrediente = get_ingrediente_id(ingrediente_id)
    return jsonify({"id": ingrediente.id, "nombre": ingrediente.nombre, "inventario": ingrediente.inventario})

@api_bp.route("/ingredientes/nombre/<string:nombre>", methods=["GET"])
def obtener_ingrediente_por_nombre(nombre):
    """Obtener un ingrediente por su nombre."""
    ingrediente = Ingrediente.query.filter_by(nombre=nombre).first()
    if not ingrediente:
        abort(404, description="Ingrediente no encontrado")
    return jsonify({"id": ingrediente.id, "nombre": ingrediente.nombre, "inventario": ingrediente.inventario})

@api_bp.route("/ingredientes/<int:ingrediente_id>/es_sano", methods=["GET"])
def es_ingrediente_sano(ingrediente_id):
    """Consultar si un ingrediente es sano por su ID."""
    ingrediente = get_ingrediente_id(ingrediente_id)
    es_sano = ingrediente.es_sano() if hasattr(ingrediente, "es_sano") else False
    return jsonify({"id": ingrediente.id, "nombre": ingrediente.nombre, "es_sano": es_sano})

@api_bp.route("/ingredientes/<int:ingrediente_id>/renovar_inventario", methods=["POST"])
def renovar_inventario_ingrediente(ingrediente_id):
    """Renovar el inventario de un ingrediente por su ID."""
    ingrediente = get_ingrediente_id(ingrediente_id)
    if hasattr(ingrediente, "renovar_inventario"):
        ingrediente.renovar_inventario()
        db.session.commit()
        return jsonify({"mensaje": f"Inventario de {ingrediente.nombre} renovado"}), 200
    else:
        abort(400, description="Este ingrediente no tiene inventario renovable")