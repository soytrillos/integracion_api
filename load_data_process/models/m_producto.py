import config.db as db
from sqlalchemy import Column, Integer, String, Float

class Producto(db.Base):
    __tablename__ = 'productos_wms'
    id = Column(Integer, primary_key=True)
    default_code = Column(String, nullable=True)
    barcode = Column(String, nullable=False)
    name = Column(String, nullable=True)
    categoria = Column(String, nullable=True)
    precio = Column(Float, nullable=True)
    costo = Column(Float, nullable=False)
    unidad_venta = Column(String, nullable=True)
    iva_venta = Column(Float, nullable=True)
    tipo_producto = Column(String, nullable=False, default='product')
    volumen = Column(Float, nullable=False)
    peso = Column(Float, nullable=True)
    lote = Column(String, nullable=True, default='none')
    vence = Column(Integer, nullable=True)