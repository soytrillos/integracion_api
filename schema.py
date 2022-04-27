from typing import Generic, Optional, TypeVar, Dict, List
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    parameter: Parameter = Field(...)


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None
    
class TokenResponse(BaseModel):
    access_token :str
    token_type: str

class ProductosBase(BaseModel):
    default_code: str
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

class RPCProductosBase(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str
    productos: List[ProductosBase]

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

class RPCClientesBase(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str
    clientes: List[ClientesBase]  

class RPCProveedoresBase(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str
    proveedores: List[ProveedoresBase]  

class RPCCredencialBase(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str

class ItemsCompraBase(BaseModel):
    product_id: str
    product_qty: float
    taxes_id: float
    price_unit: float

class ComprasBase(RPCCredencialBase):
    name: str
    partner_id: str
    partner_ref: str
    date_planned: str
    detalle: List[ItemsCompraBase]

class ItemsVentaBase(BaseModel):
    product_id: str
    product_uom_qty: float
    tax_id: float
    price_unit: float
    discount: float

class VentasBase(RPCCredencialBase):
    name: str
    partner_id: str
    date_order: str
    detalle: List[ItemsVentaBase]