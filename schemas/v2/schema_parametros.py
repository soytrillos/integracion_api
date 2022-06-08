from typing import Generic, Optional, TypeVar, Dict, List
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

class _LocalizacionBase(BaseModel):
    name: str
    barcode: str
    localizacion_padre: str
   
class _LocalizacionRPC(BaseModel):
    url_rpc: str
    db_rpc: str
    email_rpc: str
    token_rpc: str
    clientes: List[_LocalizacionBase]

