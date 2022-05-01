import config.db as db
from sqlalchemy import Column, Integer, String, Float

class Proveedor(db.Base):
    __tablename__ = 'proveedores_wms'
    id = Column(Integer, primary_key=True)
    identificacion = Column(String, nullable=True)
    tipo_identificacion = Column(String, nullable=True)
    nombre_completo = Column(String, nullable=True)
    correo = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    zona = Column(String, nullable=False)
    codigo_postal = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    departamento = Column(String, nullable=True)
    pais = Column(String, nullable=True)