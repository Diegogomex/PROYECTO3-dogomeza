from app.models.base import Base
from app.models.complemento import Complemento
from app.models.copa import Copa
from app.models.malteada import Malteada
from app.models.heladeria import Heladeria
from app.models.producto import Producto
from sqlalchemy.orm import joinedload

class HeladeriaController:
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.heladeria = Heladeria("DG Heladería")
        self._agregar_productos()

    def _agregar_productos(self):
        with self.app.app_context():
            # Verificar si ya existen productos en la base de datos
            if Producto.query.count() == 0:
                # Ingredientes
                helado_de_vainilla = Base(nombre="Helado de Vainilla", precio=1200, calorias=100, inventario=2.0, es_vegetariano=False, sabor="vainilla")
                helado_de_chocolate = Base(nombre="Helado de Chocolate", precio=1500, calorias=250, inventario=6.0, es_vegetariano=False, sabor="chocolate")
                frutas_mixtas = Base(nombre="Frutas mixtas", precio=2000, calorias=50, inventario=0.0, es_vegetariano=True, sabor="fruta")
                fresas = Base(nombre="Fresas", precio=1500, calorias=35, inventario=3.0, es_vegetariano=True, sabor="fresa")
                mani_japones = Complemento(nombre="Mani Japones", precio=700, calorias=35, inventario=6.0, es_vegetariano=True)
                sirope_de_caramelo = Complemento(nombre="Sirope de Caramelo", precio=1000, calorias=200, inventario=2.0, es_vegetariano=False)
                sirope_de_fresa = Complemento(nombre="Sirope de Fresa", precio=1000, calorias=200, inventario=8.0, es_vegetariano=False)
                crema_de_leche = Complemento(nombre="Crema de Leche", precio=700, calorias=150, inventario=7.0, es_vegetariano=False)
                nuez_moscada = Complemento(nombre="Nuez Moscada", precio=700, calorias=40, inventario=1.0, es_vegetariano=True)

                # Productos
                malteada_de_vainilla = Malteada(nombre="Malteada De Vainilla", precio_publico=7500, ingredientes=[helado_de_vainilla, sirope_de_fresa, mani_japones], volumen=7)
                malteada_choconuez = Malteada(nombre="Malteada Choconuez", precio_publico=10000, ingredientes=[helado_de_chocolate, nuez_moscada, sirope_de_caramelo], volumen=8)
                champions_de_frutas = Copa(nombre="Champions De Frutas", precio_publico=7000, ingredientes=[frutas_mixtas, crema_de_leche, sirope_de_caramelo], tipo_vaso="Vaso de Vidrio")
                explosion_de_fresa = Copa(nombre="Explosion De Fresa", precio_publico=5000, ingredientes=[fresas, crema_de_leche, sirope_de_fresa], tipo_vaso="Vaso de Plástico")

                # Guardar en la base de datos
                self.db.session.add_all([helado_de_vainilla, helado_de_chocolate, frutas_mixtas, fresas, mani_japones, sirope_de_caramelo, sirope_de_fresa, crema_de_leche, nuez_moscada])
                self.db.session.add_all([malteada_de_vainilla, malteada_choconuez, champions_de_frutas, explosion_de_fresa])
                self.db.session.commit()

            # Agregar productos a la heladería (recuperados desde la base de datos)
            productos = Producto.query.options(joinedload(Producto.ingredientes)).all()
            for producto in productos:
                self.heladeria.agregar_producto(producto)

    def listar_productos(self):
        """
        Lista todos los productos disponibles en la base de datos.
        Retorna:
        - list: Lista de productos.
        """
        with self.app.app_context():
            return Producto.query.options(joinedload(Producto.ingredientes)).all()

    def transformar_nombre_producto(self, nombre_producto: str) -> str:
        """
        Transforma un nombre de producto de formato URL a formato legible.
        Parámetro:
        - nombre_producto (str): Nombre del producto en formato URL.
        Retorna:
        - str: Nombre del producto en formato legible.
        """
        return nombre_producto.replace('-', ' ').title()

    def vender_producto(self, nombre_producto: str) -> str:
        """
        Intenta vender un producto y maneja los errores.
        Parámetro:
        - nombre_producto (str): Nombre del producto a vender.
        Retorna:
        - str: Mensaje de éxito o error.
        """
        try:
            nombre_producto_correcto = self.transformar_nombre_producto(nombre_producto)
            with self.app.app_context():
                # Recuperar el producto con sus ingredientes cargados
                producto = Producto.query.filter_by(nombre=nombre_producto_correcto).options(joinedload(Producto.ingredientes)).first()
                if not producto:
                    return f"¡Oh no! El producto '{nombre_producto_correcto}' no existe.", 404
                
                # Intentar vender el producto
                resultado = self.heladeria.vender(producto, self.db.session)
                return resultado  # Retorna "Vendido!!!" si la venta es exitosa
        except ValueError as e:
            return f"¡Oh no! Nos hemos quedado sin ingredientes: {str(e)}"
