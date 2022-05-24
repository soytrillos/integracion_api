import fastapi
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from schemas.v2.schema_maestras import _ProductosRPC, _ClientesRPC, _ProveedoresRPC
from services.v2.productos_wms import maestra_productos
from services.v2.clientes_wms import maestra_clientes
from services.v2.proveedor_wms import maestra_proveedores

router = APIRouter()

"""
    Productos Router

"""

@router.post("/v2/productos", tags=["maestrasv2"])
async def m_productos(producto: _ProductosRPC):
    matrix_return = {}
    matrix_return = []
    result = producto.dict()
    cls_product = maestra_productos(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    cred = cls_product.cliente_rpc()
    if cred != False:
        for product in result['productos']:
            search = cls_product.consulta_producto(cred[0], cred[1], product['default_code'])
            if search == []:
                creacion = cls_product.crear_producto(cred[0], cred[1], product)
                matrix_return.append(creacion)
            else:
                actualizar = cls_product.actualizar_producto(cred[0], cred[1], product, search[0]['id'])
                matrix_return.append(actualizar)
            response_find = str(matrix_return).find('error')    
        
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=matrix_return
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_return
            )
    else:
        matrix_return.append({'error': 'Error credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_return
        )

"""
    Clientes Router

"""

@router.post("/v2/clientes", tags=["maestrasv2"])
async def m_clientes(cliente: _ClientesRPC):
    matrix_return = {}
    matrix_return = []
    result = cliente.dict()
    cls_client = maestra_clientes(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    cred = cls_client.cliente_rpc()
    if cred != False:
        for client in result['clientes']:
            search = cls_client.consulta_cliente(cred[0], cred[1], client['vat'])
            if search == []:
                creacion = cls_client.crear_cliente(cred[0], cred[1], client)
                matrix_return.append(creacion)
            else:
                actualizar = cls_client.actualizar_cliente(cred[0], cred[1], client, search[0]['id'])
                matrix_return.append(actualizar)

        response_find = str(matrix_return).find('error') 
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=matrix_return
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_return
            )
    else:
        matrix_return.append({'error': 'Error credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_return
        )

"""
    Proveedores Router

"""

@router.post("/v2/proveedores", tags=["maestrasv2"])
async def m_proveedores(proveedor: _ProveedoresRPC):
    matrix_return = {}
    matrix_return = []
    result = proveedor.dict()
    cls_proveedor = maestra_proveedores(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    cred = cls_proveedor.cliente_rpc()
    if cred != False:
        for client in result['proveedores']:
            search = cls_proveedor.consulta_proveedor(cred[0], cred[1], client['vat'])
            if search == []:
                creacion = cls_proveedor.crear_proveedor(cred[0], cred[1], client)
                matrix_return.append(creacion)
            else:
                actualizar = cls_proveedor.actualizar_proveedor(cred[0], cred[1], client, search[0]['id'])
                matrix_return.append(actualizar)

        response_find = str(matrix_return).find('error') 
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=matrix_return
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_return
            )
    else:
        matrix_return.append({'error': 'Error credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_return
        )
