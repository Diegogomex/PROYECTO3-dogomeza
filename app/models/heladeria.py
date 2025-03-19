from app.models.producto import Producto
from app.models.ingrediente import Ingrediente
from app.models.base import Base
from app.models.complemento import Complemento
from sqlalchemy.orm import joinedload

class Heladeria:
    def __init__(self, nombre: str) -> None:
        """
        Inicializa una instancia de Heladeria.
        Parámetro:
        - nombre (str): Nombre de la heladería.
        """
        self.__nombre = nombre
        self.__productos = []
        self.__inventario = []
        self.__ventas_dia = 0

    def producto_mas_rentable(self) -> Producto:
        """
        Determina el producto más rentable de la heladería.
        Retorna:
        - Producto: El producto más rentable.
        """
        if not self.__productos:
            return None
        return max(self.__productos, key=lambda p: p.calcular_rentabilidad())

    def agregar_producto(self, producto: Producto) -> None:
        """
        Agrega un producto a la lista de productos.
        Parámetro:
        - producto (Producto): Producto a agregar.
        """
        if len(self.__productos) >= 4:
            raise ValueError("Ya hay 4 productos, no se pueden agregar más.")
        self.__productos.append(producto)

    def eliminar_producto(self, producto: Producto) -> None:
        """
        Elimina un producto de la lista de productos.
        Parámetro:
        - producto (Producto): Producto a eliminar.
        """
        self.__productos.remove(producto)

    def listar_productos(self) -> list:
        """
        Lista todos los productos de la heladería.
        Retorna:
        - list: Lista de productos.
        """
        return self.__productos

    def vender(self, producto: Producto, session) -> str:
        """
        Vende un producto si hay existencias suficientes.
        Parámetros:
        - producto (Producto): Producto a vender.
        - session: Sesión de SQLAlchemy para manejar transacciones.
        Retorna:
        - str: Mensaje de éxito o error.
        """
        if not self.__productos:
            raise ValueError("No hay productos disponibles en la heladería.")

        # Verificar que el producto pertenezca a la heladería usando su ID
        if producto.id not in [p.id for p in self.__productos]:
            raise ValueError(f"El producto '{producto.nombre}' no está disponible en esta heladería.")

        # Definir las cantidades necesarias
        necesario_base = 0.2
        necesario_complemento = 1

        # Cargar los ingredientes del producto dentro del contexto de la sesión
        with session.no_autoflush:
            # Recargar el producto desde la base de datos para asegurar que esté vinculado a la sesión
            producto = session.get(Producto, producto.id, options=[joinedload(Producto.ingredientes)])

            if not producto:
                raise ValueError(f"El producto '{producto.nombre}' no existe.")

            # Verificar existencias de ingredientes
            ingredientes_faltantes = []
            print(f"Verificando inventario para {producto.nombre}:")
            for ingrediente in producto.ingredientes:
                print(f"- Ingrediente: {ingrediente.nombre}, Tipo: {type(ingrediente)}, Inventario: {ingrediente.inventario}")
                if isinstance(ingrediente, Base):
                    print(f"  - Tipo: Base, Necesario: {necesario_base}")
                    if ingrediente.inventario < necesario_base:
                        print(f"  - ¡Falta base! Agregando '{ingrediente.nombre}' a la lista de faltantes.")
                        ingredientes_faltantes.append(ingrediente.nombre)
                elif isinstance(ingrediente, Complemento):
                    print(f"  - Tipo: Complemento, Necesario: {necesario_complemento}")
                    if ingrediente.inventario < necesario_complemento:
                        print(f"  - ¡Falta complemento! Agregando '{ingrediente.nombre}' a la lista de faltantes.")
                        ingredientes_faltantes.append(ingrediente.nombre)
                else:
                    print(f"  - ¡Tipo desconocido! No se puede verificar el inventario.")

            # Si hay ingredientes faltantes, lanzar un error
            if ingredientes_faltantes:
                mensaje_error = f"Falta de ingrediente(s): {', '.join(ingredientes_faltantes)}"
                print(f"¡Venta cancelada! Razón: {mensaje_error}")
                raise ValueError(mensaje_error)

            # Restar las cantidades necesarias de cada ingrediente
            print(f"Actualizando inventario para {producto.nombre}:")
            for ingrediente in producto.ingredientes:
                if isinstance(ingrediente, Base):
                    ingrediente.inventario -= necesario_base
                    print(f"- Base ({ingrediente.nombre}): Nuevo inventario: {ingrediente.inventario}")
                elif isinstance(ingrediente, Complemento):
                    ingrediente.inventario -= necesario_complemento
                    print(f"- Complemento ({ingrediente.nombre}): Nuevo inventario: {ingrediente.inventario}")

        # Sumar a las ventas del día el precio del producto
        self.__ventas_dia += producto.precio_publico

        # Confirmar la transacción
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return f"Error al confirmar la transacción: {str(e)}"

        return "Vendido!!!"

    def agregar_ingrediente(self, ingrediente: Ingrediente) -> None:
        """
        Agrega un ingrediente a la lista de inventario.
        Parámetro:
        - ingrediente (Ingrediente): Ingrediente a agregar.
        """
        self.__inventario.append(ingrediente)

    def listar_ingredientes(self) -> list:
        """
        Lista todos los ingredientes en el inventario.
        Retorna:
        - list: Lista de ingredientes.
        """
        return self.__inventario

    @property
    def nombre(self) -> str:
        """Devuelve el valor del atributo privado 'nombre'."""
        return self.__nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        """
        Establece un nuevo valor para el atributo privado 'nombre'.
        Valida que el valor enviado corresponda al tipo de dato del atributo.
        """
        if isinstance(value, str):
            self.__nombre = value
        else:
            raise ValueError("Expected str")

    @property
    def productos(self) -> list:
        """Devuelve el valor del atributo privado 'productos'."""
        return self.__productos

    @productos.setter
    def productos(self, value: list) -> None:
        """
        Establece un nuevo valor para el atributo privado 'productos'.
        Valida que el valor enviado corresponda al tipo de dato del atributo.
        """
        if len(value) > 4:
            raise ValueError("No se pueden tener más de 4 productos.")
        if all(isinstance(producto, Producto) for producto in value):
            self.__productos = value
        else:
            raise ValueError("Expected list of Producto")

    @property
    def inventario(self) -> list:
        """Devuelve el valor del atributo privado 'inventario'."""
        return self.__inventario

    @inventario.setter
    def inventario(self, value: list) -> None:
        """
        Establece un nuevo valor para el atributo privado 'inventario'.
        Valida que el valor enviado corresponda al tipo de dato del atributo.
        """
        if all(isinstance(ingrediente, Ingrediente) for ingrediente in value):
            self.__inventario = value
        else:
            raise ValueError("Expected list of Ingrediente")

    @property
    def ventas_dia(self) -> int:
        """Devuelve el valor del atributo privado 'ventas_dia'."""
        return self.__ventas_dia

    @ventas_dia.setter
    def ventas_dia(self, value: int) -> None:
        """
        Establece un nuevo valor para el atributo privado 'ventas_dia'.
        Valida que el valor enviado corresponda al tipo de dato del atributo.
        """
        if isinstance(value, int):
            self.__ventas_dia = value
        else:
            raise ValueError("Expected int")
