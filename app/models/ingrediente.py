from app.config.db import db
from app.models.producto_ingrediente import producto_ingrediente

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Float, nullable=False)
    es_vegetariano = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.String(50))

    # Relación con la tabla de productos
    productos = db.relationship('Producto', secondary=producto_ingrediente, back_populates='ingredientes')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'ingrediente'
    }

    def __repr__(self):
        return f'<Ingrediente {self.nombre}>'
