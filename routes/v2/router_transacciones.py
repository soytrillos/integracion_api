import fastapi
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from schemas.v2.schema_transacciones import _TransferenciasRPC
from services.v2.transacciones_wms import maestro_transacciones

router = APIRouter()

"""
    Transacciones Router

"""
@router.post("/v2/consulta_tr_internas", summary="Busqueda transferencias", tags=["transaccionesv2"]) #, deprecated=True)
async def search_tr_interna_s(tr_interna_s: _TransferenciasRPC):
    result = tr_interna_s.dict()
    matrix_errores = {}

    cls_tr_interno_c = maestro_transacciones(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_tr_interno_c.conexion_rpc()

    if conexion_rpc[1] != False:
        resultado = cls_tr_interno_c.transferencias_internas_s(conexion_rpc[0], conexion_rpc[1])
        raise fastapi.HTTPException(
            status_code=200, detail=resultado
        )

    else:
        matrix_errores['error_rpc'] = []
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )

@router.post("/v2/creacion_tr_internas", tags=["transaccionesv2"])
async def create_tr_interna_c(tr_interna_c: _TransferenciasRPC):
    result = tr_interna_c.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []

    cls_tr_interno_c = maestro_transacciones(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_tr_interno_c.conexion_rpc()

    if conexion_rpc[1] != False:
        resultado = cls_tr_interno_c.transferencias_internas_c(conexion_rpc[0], conexion_rpc[1], result)
        response_find = str(resultado).find('error') 
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=resultado
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=resultado
            )

    else:
        matrix_errores['error_rpc'] = []
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )

"""
@router.post("/consulta_devolucion_mercancia") #, dependencies=[Depends(JWTBearer())])
async def consulta_devolucion_m(dv_mercancia: RPCCredencialBase):
    result = dv_mercancia.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []

    cls_dv_mercancia_s = maestro_transacciones(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_dv_mercancia_s.conexion_rpc()

    if conexion_rpc[1] != False:
        resultado = cls_dv_mercancia_s.devolucion_mercancia_s(conexion_rpc[0], conexion_rpc[1])
        response_find = str(resultado).find('error') 
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=resultado
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=resultado
            )

    else:
        matrix_errores['error_rpc'] = []
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )

@router.post("/creacion_devolucion_mercancia") #, dependencies=[Depends(JWTBearer())])
async def create_devolucion_m(dv_mercancia_c: DevolucionBase):
    result = dv_mercancia_c.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []

    cls_dv_mercancia_c = maestro_transacciones(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_dv_mercancia_c.conexion_rpc()

    if conexion_rpc[1] != False:
        resultado = cls_dv_mercancia_c.devolucion_mercancia_c(conexion_rpc[0], conexion_rpc[1], result)
        response_find = str(resultado).find('error') 
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=resultado
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=resultado
            )

    else:
        matrix_errores['error_rpc'] = []
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )

@router.post("/creacion_min_max") #, dependencies=[Depends(JWTBearer())])
async def create_minmax_m(min_max_c: MinMaxBase):
    result = min_max_c.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []

    cls_min_max_c = maestro_transacciones(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_min_max_c.conexion_rpc()

    if conexion_rpc[1] != False:
        resultado = cls_min_max_c.create_min_max(conexion_rpc[0], conexion_rpc[1], result)
        response_find = str(resultado).find('error') 
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=resultado
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=resultado
            )

    else:
        matrix_errores['error_rpc'] = []
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )

@router.post("/creacion_proveedor_producto") #, dependencies=[Depends(JWTBearer())])
async def create_proveedor_pro(proveedor_pro_c: SupplierProductBase):
    result = proveedor_pro_c.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []

    cls_proveedor_pro_c = maestro_transacciones(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_proveedor_pro_c.conexion_rpc()

    if conexion_rpc[1] != False:
        resultado = cls_proveedor_pro_c.supplier_product(conexion_rpc[0], conexion_rpc[1], result)
        response_find = str(resultado).find('error') 
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=resultado
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=resultado
            )

    else:
        matrix_errores['error_rpc'] = []
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )
        
@router.post("/ajuste_inventario")
async def create_aj_inv(ajuste_schema: AjusteInventarioBase):
    result = ajuste_schema.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []
    
    cls_ajuste_c = maestro_transacciones(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_ajuste_c.conexion_rpc()
    
    if conexion_rpc[1] != False:
        resultado = cls_ajuste_c.ajuste_inventario_v1_c(conexion_rpc[0], conexion_rpc[1], result)
        response_find = str(resultado).find('error') 
        if response_find == -1:
            raise fastapi.HTTPException(
                status_code=200, detail=resultado
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=resultado
            )
            
"""