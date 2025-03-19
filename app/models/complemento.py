from app.models.ingrediente import Ingrediente

class Complemento(Ingrediente):
    __mapper_args__ = {
        'polymorphic_identity': 'complemento'
    }

    def __init__(self, nombre:str, precio:int, calorias:int, inventario:float, es_vegetariano:bool)->None:
        super().__init__(nombre=nombre, precio=precio, calorias=calorias, inventario=inventario, es_vegetariano=es_vegetariano)
    
    def abastecer(self, cantidad:float)->None:
        """ Abastece el inventario de la base sumando 10. """
        if isinstance(cantidad,(int, float)):
            self.inventario += 10
        else:
            raise ValueError ("La cantidad debe ser un número .")

    def renovar_inventario (self)->None:
        """ Renueva el inventario del complemento a 0.0 """
        self.inventario = 0.0 
    
