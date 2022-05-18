from fastapi import APIRouter, Depends
import fastapi
from schema import RequestSchema, ResponseSchema, TokenResponse, RPCProductosBase, RPCClientesBase, RPCProveedoresBase, RPCCredencialBase, ComprasBase, VentasBase, TransferenciaInternaBase, DevolucionBase, MinMaxBase, SupplierProductBase, AjusteInventarioBase
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from repository import JWTRepo, JWTBearer, UsersRepo
from model import Users
from datetime import datetime, timedelta
from fastapi.responses import FileResponse, JSONResponse

from services.productos_wms import maestra_productos
from services.clientes_wms import maestra_clientes
from services.proveedor_wms import maestra_proveedores
from services.compras_wms import maestro_compras
from services.ventas_wms import maestro_ventas
from services.transacciones_wms import maestro_transacciones

router = APIRouter()

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
    Authentication Router

"""

@router.post('/signup')
async def signup(request: RequestSchema, db: Session = Depends(get_db)):
    try:
        # insert user to db
        _user = Users(username=request.parameter.data["username"],
                      email=request.parameter.data["email"],
                      phone_number=request.parameter.data["phone_number"],
                      password=pwd_context.hash(
                          request.parameter.data["password"]),
                      first_name=request.parameter.data['first_name'],
                      last_name=request.parameter.data['last_name'])
        UsersRepo.insert(db, _user)
        return ResponseSchema(code="200", status="Ok", message="Success save data").dict(exclude_none=True)
    except Exception as error:
        return ResponseSchema(code="500", status="Error", message=error.args).dict(exclude_none=True)


@router.post('/login')
async def login(request: RequestSchema, db: Session = Depends(get_db)):
    try:
       # find user by username
        _user = UsersRepo.find_by_username(
            db, Users, request.parameter.data["username"])

        if not pwd_context.verify(request.parameter.data["password"], _user.password):
            return ResponseSchema(code="400", status="Bad Request", message="Invalid password").dict(exclude_none=True)

        token = JWTRepo.generate_token({"sub": _user.username})
        return ResponseSchema(code="200", status="OK", message="success login!", result=TokenResponse(access_token=token, token_type="Bearer")).dict(exclude_none=True)
    except Exception as error:
        error_message = str(error.args)
        return ResponseSchema(code="500", status="Internal Server Error", message=error_message).dict(exclude_none=True)


"""
    Users Router

"""

@router.get("/users", dependencies=[Depends(JWTBearer())])
async def retrieve_all(db: Session = Depends(get_db)):
    _user = UsersRepo.retrieve_all(db, Users)
    return ResponseSchema(code="200", status="Ok", message="Sucess retrieve data", result=_user).dict(exclude_none=True)


"""
    Productos Router

"""

@router.post("/productos", dependencies=[Depends(JWTBearer())])
async def m_product(producto: RPCProductosBase):
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

@router.post("/clientes", dependencies=[Depends(JWTBearer())])
async def m_client(cliente: RPCClientesBase):
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

@router.post("/proveedores", dependencies=[Depends(JWTBearer())])
async def m_supplier(proveedor: RPCProveedoresBase):
    matrix_return = {}
    matrix_return = []
    result = proveedor.dict()
    cls_client = maestra_proveedores(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    cred = cls_client.cliente_rpc()
    if cred != False:
        for client in result['proveedores']:
            search = cls_client.consulta_proveedor(cred[0], cred[1], client['vat'])
            if search == []:
                creacion = cls_client.crear_proveedor(cred[0], cred[1], client)
                matrix_return.append(creacion)
            else:
                actualizar = cls_client.actualizar_proveedor(cred[0], cred[1], client, search[0]['id'])
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
    Compras Router

"""

@router.post("/consulta_compras") #, dependencies=[Depends(JWTBearer())])
async def search_compra(compras: RPCCredencialBase):
    result = compras.dict()
    matrix_errores = {}
    
    cls_compra = maestro_compras(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_compra.conexion_rpc()
    if conexion_rpc[1] != False:
        encabezado = cls_compra.purchase_order_s(conexion_rpc[0], conexion_rpc[1])
        compras_dict = {}
        for en_compra in encabezado:
            cliente = cls_compra.clientes_rpc(conexion_rpc[0], conexion_rpc[1], en_compra['partner_id'][0])
            compras_dict[en_compra["name"]] = []
            compras_dict[en_compra["name"]] = {
                    'id': en_compra['id'], 
                    'name': en_compra['name'], 
                    'partner_id': cliente[0]['vat'], 
                    'partner_ref': en_compra['partner_ref'], 
                    'date_approve': en_compra['date_approve'],
                    'almacen': en_compra['picking_type_id'][1],
                    'compañia': en_compra['company_id'][1]
                }
            detalle = cls_compra.purchase_order_line_s(conexion_rpc[0], conexion_rpc[1], en_compra['id'])
            compras_dict[en_compra["name"]]['detalle'] = []
            for det_compra in detalle:
                producto = cls_compra.productos_rpc(conexion_rpc[0], conexion_rpc[1], det_compra['product_id'][0])
                iva = cls_compra.iva_rpc(conexion_rpc[0], conexion_rpc[1], det_compra['taxes_id'][0])
                compras_dict[en_compra["name"]]['detalle'].append({
                        'product_id': producto[0]['default_code'],
                        'product_qty': det_compra['product_qty'],
                        'taxes_id': iva[0]['amount'],
                        'price_unit': det_compra['price_unit']
                    }
                )
            
        raise fastapi.HTTPException(
            status_code=200, detail=compras_dict
        )
    else:    
        matrix_errores['error_rpc'] = []
        matrix_errores['error_rpc'].append({'code': 401, 'msg': 'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )


@router.post("/creacion_compras")
async def create_compra(compra: ComprasBase):
    result = compra.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []
    matrix_productos = {}
    matrix_productos = []

    cls_compra = maestro_compras(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_compra.conexion_rpc()
    
    if conexion_rpc[1] != False:
        matrix_errores['error_maestras'] = []
        try:
            x_cl = maestra_clientes(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
            cred = x_cl.cliente_rpc()
            search_cli = x_cl.consulta_cliente(cred[0], cred[1], result['partner_id'])
            cliente = search_cli[0]['id']
        except Exception as error:
            matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Cliente "{result["partner_id"]}" no existe'})
            cliente = ''
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_errores
            )

        for impuesto in result['detalle']:
            iva = cls_compra.iva_producto(cred[0], cred[1], impuesto["taxes_id"])
            if iva == []:
                matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Impuesto "{impuesto["taxes_id"]}", del producto {impuesto["product_id"]} no existe'})
            else:
                iva = iva[0]['id']

        try:
            documento = cls_compra.validacion_documento(conexion_rpc[0], conexion_rpc[1], result)
            if documento != {'documento': []}:
                matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Documento "{result["name"]}" ya existe'})
            else:
                cl_x = maestra_productos(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
                cred = cl_x.cliente_rpc()
                for product in result['detalle']:
                    search_pro = cl_x.consulta_producto(cred[0], cred[1], product['product_id'])
                    if search_pro == []:
                        matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Producto "{product["product_id"]}" no existe'})
                    else:
                        producto = search_pro[0]['id']
                        matrix_productos.append({'producto': producto})

                if matrix_errores['error_maestras'] == []:
                    encabezado = cls_compra.purchase_order_c(conexion_rpc[0], conexion_rpc[1], result, cliente)
                    for detalle in result['detalle']:
                        detalles = cls_compra.purchase_order_line_c(conexion_rpc[0], conexion_rpc[1], detalle, encabezado, detalle['product_id'])
        except Exception as error:
            matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Error {error}'})
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_errores
            )

        if matrix_errores['error_maestras'] == []:
            raise fastapi.HTTPException(
                status_code=200, detail=result
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_errores
            )
    else:
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )


"""
    Ventas Router

"""

@router.post("/consulta_ventas") #, dependencies=[Depends(JWTBearer())])
async def search_venta(ventas: RPCCredencialBase):
    result = ventas.dict()
    matrix_errores = {}

    cls_venta = maestro_ventas(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_venta.conexion_rpc()

    if conexion_rpc[1] != False:
        ventas_dict = {}
        encabezado = cls_venta.sale_order_s(conexion_rpc[0], conexion_rpc[1])
        for en_venta in encabezado:
            cliente = cls_venta.clientes_rpc(conexion_rpc[0], conexion_rpc[1], en_venta['partner_id'][0])
            ventas_dict[f'{en_venta["name"]}'] = []
            ventas_dict[f'{en_venta["name"]}'] = {
                    'id': en_venta['id'], 
                    'name': en_venta['name'], 
                    'partner_id': cliente[0]['vat'],
                    'date_order': en_venta['date_order'],
                    'almacen': en_venta['warehouse_id'][1],
                    'compañia': en_venta['company_id'][1]
                }
            detalle = cls_venta.sale_order_line_s(conexion_rpc[0], conexion_rpc[1], en_venta['id'])
            ventas_dict[f'{en_venta["name"]}']['detalle'] = []
            for det_compra in detalle:
                producto = cls_venta.productos_rpc(conexion_rpc[0], conexion_rpc[1], det_compra['product_id'][0])
                iva = cls_venta.iva_rpc(conexion_rpc[0], conexion_rpc[1], det_compra['tax_id'][0])
                ventas_dict[f'{en_venta["name"]}']['detalle'].append({
                        'product_id': producto[0]['default_code'],
                        'product_uom_qty': det_compra['product_uom_qty'],
                        'tax_id': iva[0]['amount'],
                        'price_unit': det_compra['price_unit'],
                        'discount': det_compra['discount']
                    }
                )

        raise fastapi.HTTPException(
            status_code=200, detail=ventas_dict
        )

    else:
        matrix_errores['error_rpc'] = []
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )


@router.post("/creacion_ventas")
async def create_venta(venta: VentasBase):
    result = venta.dict()
    matrix_errores = {}
    matrix_errores['error_rpc'] = []

    matrix_productos = {}
    matrix_productos = []

    cls_venta = maestro_ventas(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
    conexion_rpc = cls_venta.conexion_rpc()

    if conexion_rpc[1] != False:
        matrix_errores['error_maestras'] = []
        try:
            x_cl = maestra_clientes(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
            cred = x_cl.cliente_rpc()
            search_cli = x_cl.consulta_cliente(cred[0], cred[1], result['partner_id'])
            cliente = search_cli[0]['id']
        except Exception as error:
            matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Cliente "{result["partner_id"]}" no existe'})
            cliente = ''
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_errores
            )

        for impuesto in result['detalle']:
            iva = cls_venta.iva_producto(cred[0], cred[1], impuesto["tax_id"])
            if iva == []:
                matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Impuesto "{impuesto["tax_id"]}", del producto {impuesto["product_id"]} no existe'})
            else:
                iva = iva[0]['id']


        try:
            documento = cls_venta.validacion_documento(conexion_rpc[0], conexion_rpc[1], result)
            if documento != {'documento': []}:
                matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Documento "{result["name"]}" ya existe'})
            else:
                cl_x = maestra_productos(result['url_rpc'], result['db_rpc'], result['email_rpc'], result['token_rpc'])
                cred = cl_x.cliente_rpc()
                for product in result['detalle']:
                    search_pro = cl_x.consulta_producto(cred[0], cred[1], product['product_id'])
                    if search_pro == []:
                        matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Producto "{product["product_id"]}" no existe'})
                    else:
                        producto = search_pro[0]['id']
                        matrix_productos.append({'producto': producto})

                if matrix_errores['error_maestras'] == []:
                    encabezado = cls_venta.sale_order_c(conexion_rpc[0], conexion_rpc[1], result, cliente)
                    for detalle in result['detalle']:
                        detalles = cls_venta.sale_order_line_c(conexion_rpc[0], conexion_rpc[1], detalle, encabezado, detalle['product_id'])
        except Exception as error:
            matrix_errores['error_maestras'].append({'code': 400, 'msg': f'Error {error}'})
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_errores
            )

        if matrix_errores['error_maestras'] == []:
            raise fastapi.HTTPException(
                status_code=200, detail=result
            )
        else:
            raise fastapi.HTTPException(
                status_code=400, detail=matrix_errores
            )

    else:
        matrix_errores['error_rpc'].append({'code': 401, 'msg': f'Error en las credenciales RPC'})
        raise fastapi.HTTPException(
            status_code=401, detail=matrix_errores
        )


"""
    Transacciones Router

"""
@router.post("/consulta_tr_internas") #, dependencies=[Depends(JWTBearer())])
async def search_tr_interna_s(tr_interna_s: RPCCredencialBase):
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

@router.post("/creacion_tr_internas") #, dependencies=[Depends(JWTBearer())])
async def create_tr_interna_c(tr_interna_c: TransferenciaInternaBase):
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