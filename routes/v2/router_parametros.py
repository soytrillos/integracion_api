import fastapi
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from schemas.v2.schema_parametros import _LocalizacionRPC
from services.v2.parametros_wms import maestra_parametros

router = APIRouter()

"""
    Parametros Router

"""
@router.post("/v2/creacion_localizacion", tags=["Parametrosv2"])
async def create_localizacion(localizacion_c: _LocalizacionRPC):
    result = localizacion_c.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []

    localizacion_interno_c = maestra_parametros(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = localizacion_interno_c.cliente_rpc()

    if conexion_rpc[1] != False:
        resultado = localizacion_interno_c.creacion_localizacion(conexion_rpc[0], conexion_rpc[1], result)
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