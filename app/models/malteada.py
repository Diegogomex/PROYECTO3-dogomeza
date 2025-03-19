from app.config.db import db
from app.models.producto import Producto

class Malteada(Producto):
    __tablename__ = None  
    __mapper_args__ = {
        'polymorphic_identity': 'malteada' 
    }

    volumen = db.Column(db.Integer)

    
    def calcular_calorias(self) -> float:
        """
        Calcula las calorías de la malteada sumando las calorías de los ingredientes.
        """
        return sum(ingrediente.calorias for ingrediente in self.ingredientes)

    def calcular_costo(self) -> int:
        """
        Calcula el costo de la malteada sumando los precios de los ingredientes.
        """
        return sum(ingrediente.precio for ingrediente in self.ingredientes)
    
    def calcular_rentabilidad(self) -> int:
        """
        Calcula la rentabilidad de la malteada restando el costo de los ingredientes al precio público.
        """
        return self.precio_publico - self.calcular_costo()

    def __repr__(self):
        return f'<Malteada {self.nombre}>'