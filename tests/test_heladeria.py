import unittest
from app.models.heladeria import Heladeria
from app.models.base import Base
from app.models.complemento import Complemento
from app.models.copa import Copa
from app.models.malteada import Malteada
from app.config.db import db
from app import create_app

class TestHeladeria(unittest.TestCase):
    def setUp(self):
        # Configurar la aplicación y la base de datos para pruebas
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crear una instancia de Heladeria
        self.heladeria = Heladeria("DG Heladería")

        # Crear ingredientes de prueba
        self.ingrediente1 = Base(nombre="Helado de Vainilla", precio=1200, calorias=100, inventario=2.0, es_vegetariano=False, sabor="vainilla")
        self.ingrediente2 = Complemento(nombre="Sirope de Fresa", precio=1000, calorias=200, inventario=8.0, es_vegetariano=False)

        # Guardar los ingredientes en la base de datos
        db.session.add(self.ingrediente1)
        db.session.add(self.ingrediente2)
        db.session.commit()

        # Crear productos de prueba
        self.malteada = Malteada(nombre="Malteada de Vainilla", precio_publico=7500, ingredientes=[self.ingrediente1, self.ingrediente2], volumen=7)
        self.copa = Copa(nombre="Copa de Frutas", precio_publico=5000, ingredientes=[self.ingrediente1, self.ingrediente2], tipo_vaso="Vaso de Vidrio")

        # Guardar los productos en la base de datos
        db.session.add(self.malteada)
        db.session.add(self.copa)
        db.session.commit()

        # Agregar productos a la heladería
        self.heladeria.agregar_producto(self.malteada)
        self.heladeria.agregar_producto(self.copa)


    def tearDown(self):
        # Limpiar la base de datos después de cada prueba
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_ingrediente_es_sano(self):
        """Prueba si un ingrediente es sano."""
        ingrediente_sano = Base(nombre="Fresa", precio=500, calorias=50, inventario=1.0, es_vegetariano=True, sabor="fresa")
        self.assertTrue(ingrediente_sano.es_sano())

        ingrediente_no_sano = Base(nombre="Helado de Chocolate", precio=1500, calorias=250, inventario=1.0, es_vegetariano=False, sabor="chocolate")
        self.assertFalse(ingrediente_no_sano.es_sano())

    def test_abastecer_ingrediente(self):
        """Prueba el método abastecer de un ingrediente."""
        self.ingrediente1.abastecer(5)
        self.assertEqual(self.ingrediente1.inventario, 7.0)

    def test_renovar_inventario_complemento(self):
        """Prueba el método renovar_inventario de un complemento."""
        self.ingrediente2.renovar_inventario()
        self.assertEqual(self.ingrediente2.inventario, 0.0)

    def test_calcular_calorias_malteada(self):
        """Prueba el cálculo de calorías de una malteada."""
        calorias = self.malteada.calcular_calorias()
        self.assertEqual(calorias, 300)  # 100 (Helado) + 200 (Sirope)

    def test_calcular_calorias_copa(self):
        """Prueba el cálculo de calorías de una copa."""
        calorias = self.copa.calcular_calorias()
        self.assertEqual(calorias, 300)  # 100 (Helado) + 200 (Sirope)

    def test_calcular_costo_produccion(self):
        """Prueba el cálculo del costo de producción de un producto."""
        costo = self.malteada.calcular_costo()
        self.assertEqual(costo, 2200)  # 1200 (Helado) + 1000 (Sirope)

    def test_calcular_rentabilidad(self):
        """Prueba el cálculo de la rentabilidad de un producto."""
        rentabilidad = self.malteada.calcular_rentabilidad()
        self.assertEqual(rentabilidad, 5300)  # 7500 (Precio público) - 2200 (Costo)

    def test_producto_mas_rentable(self):
        """Prueba encontrar el producto más rentable."""
        producto_rentable = self.heladeria.producto_mas_rentable()
        self.assertEqual(producto_rentable.nombre, "Malteada de Vainilla")

    def test_vender_producto_exitoso(self):
        """Prueba que la venta de un producto sea exitosa cuando hay suficientes ingredientes."""
        resultado = self.heladeria.vender(self.malteada, db.session)
        self.assertEqual(resultado, "Vendido!!!")
        self.assertEqual(self.ingrediente1.inventario, 1.8)  # Verificar que el inventario se actualizó
        self.assertEqual(self.ingrediente2.inventario, 7.0)  # Verificar que el inventario se actualizó

    def test_vender_producto_fallido(self):
        """Prueba que la venta de un producto falle cuando falta algún ingrediente."""
        # Reducir el inventario de un ingrediente para simular falta de stock
        self.ingrediente1.inventario = 0.1

        with self.assertRaises(ValueError) as context:
            self.heladeria.vender(self.malteada, db.session)
        self.assertTrue("Falta de ingrediente(s): Helado de Vainilla" in str(context.exception))

if __name__ == "__main__":
    unittest.main()