from services.productos_wms import maestra_productos
from services.clientes_wms import maestra_clientes
from services.proveedor_wms import maestra_proveedores

import os
from dotenv import load_dotenv

load_dotenv()
URL_RPC = os.getenv('url_rpc')
USER_RPC = os.getenv('email_rpc')
PASS_RPC = os.getenv('token_rpc')
DB_RPC = os.getenv('db_rpc')

# Datos prueba
productos = ['222111', '', 'Producto API UPDATE', 'UPD_CAT_API', 20000, 10200, 'Units', 5, 'product', '', 10]
clientes = ['1000644625', 'NIT', 'Simon Andres Trillos', 'simon.trillos@developtrillos.tech', '5981525', '314258054685', 'Cll 10', 'ABURRA NORTE', '5555001', 'Bello', 'Antioquia', 'Colombia']
proveedores = ['106446254', 'NIT', 'Andres Almanza', 'andres.almanza@developtrillos.tech', '4581525', '3545568054685', 'Cll 40 nv5', 'ABURRA SUR', '454001', 'La Estrella', 'Antioquia', 'Colombia']

# Productos
cl_x = maestra_productos(URL_RPC, DB_RPC, USER_RPC, PASS_RPC)
cred = cl_x.cliente_rpc()
search = cl_x.consulta_producto(cred[0], cred[1], productos[0])
if search == []:
    creacion = cl_x.crear_producto(cred[0], cred[1], productos)
    print(creacion)
else:
    actualizar = cl_x.actualizar_producto(cred[0], cred[1], productos, search[0]['id'])
    print(actualizar)


# Clientes
x_cl = maestra_clientes(URL_RPC, DB_RPC, USER_RPC, PASS_RPC)
cred = x_cl.cliente_rpc()
search = x_cl.consulta_cliente(cred[0], cred[1], clientes[0])
print(search)
if search == []:
    creacion = x_cl.crear_cliente(cred[0], cred[1], clientes)
    print(creacion)
else:
    actualizar = x_cl.actualizar_cliente(cred[0], cred[1], clientes, search[0]['id'])
    print(actualizar)


# Proveedores
l_cl = maestra_proveedores(URL_RPC, DB_RPC, USER_RPC, PASS_RPC)
cred = l_cl.cliente_rpc()
search = l_cl.consulta_proveedor(cred[0], cred[1], proveedores[0])
print(search)
if search == []:
    creacion = l_cl.crear_proveedor(cred[0], cred[1], proveedores)
    print(creacion)
else:
    actualizar = l_cl.actualizar_proveedor(cred[0], cred[1], proveedores, search[0]['id'])
    print(actualizar)