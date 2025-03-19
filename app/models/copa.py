from app.config.db import db
from app.models.producto import Producto

class Copa(Producto):
    __tablename__ = None  
    __mapper_args__ = {
        'polymorphic_identity': 'copa' 
    }

    tipo_vaso = db.Column(db.String(50))
    
    def calcular_calorias(self) -> float:
        """
        Calcula las calorías de la copa sumando las calorías de los ingredientes.
        """
        return sum(ingrediente.calorias for ingrediente in self.ingredientes)

    def calcular_costo(self) -> int:
        """
        Calcula el costo de la copa sumando los precios de los ingredientes.
        """
        return sum(ingrediente.precio for ingrediente in self.ingredientes)
    
    def __repr__(self):
        return f'<Copa {self.nombre}>'
