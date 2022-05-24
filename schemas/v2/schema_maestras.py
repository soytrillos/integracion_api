from typing import Generic, Optional, TypeVar, Dict, List
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

class ProductosBase(BaseModel):
    default_code: str
    ruta: List
    barcode: str
    name: str
    categoria: str
    precio: float
    costo: float
    unidad_venta: str
    iva_venta: int
    tipo_producto: str
    volumen: float
    peso: float
    lote: str
    vence: int
    
class ClientesBase(BaseModel):
    vat: str
    tipo_identificacion: str
    nombre_completo: str
    correo: str
    telefono: str
    celular: str
    direccion: str
    zona: str
    codigo_postal: str
    ciudad: str
    departamento: str
    pais: str
    
class ProveedoresBase(BaseModel):
    vat: str
    tipo_identificacion: str
    nombre_completo: str
    correo: str
    telefono: str
    celular: str
    direccion: str
    zona: str
    codigo_postal: str
    ciudad: str
    departamento: str
    pais: str

class _ProductosRPC(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str
    productos: List[ProductosBase]
    
class _ClientesRPC(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str
    clientes: List[ClientesBase]
    
class _ProveedoresRPC(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str
    clientes: List[ProveedoresBase]

