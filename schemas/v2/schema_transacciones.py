from typing import Generic, Optional, TypeVar, Dict, List
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

class DetalleItemBase(BaseModel):
    producto: str
    cantidad: float
    lote: int

class TransferenciaInternaBase(BaseModel):
    name: str
    origin: str
    partner_id: str
    location_id: str
    location_dest_id: str
    note: str
    detalle: List[DetalleItemBase]
    
class _TransferenciasRPC(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str
    transferencias: List[TransferenciaInternaBase]