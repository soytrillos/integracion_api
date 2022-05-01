from operator import delitem
import config.db as db
from models.m_proveedor import Proveedor
from models.m_cliente import Cliente
from models.m_producto import Producto
import csv

def proveedor_func(filename_input):
    db.session.query(Proveedor).delete()
    with open(filename_input, 'r') as file_input:
        input_data = csv.DictReader(file_input, delimiter=';')
        for datos in input_data:
            proveedor_wms = Proveedor(
                                identificacion=datos['identificacion'], 
                                tipo_identificacion=datos['tipo_identificacion'], 
                                nombre_completo=datos['nombre_completo'], 
                                correo=datos['correo'],
                                telefono=datos['telefono'],
                                celular=datos['celular'],
                                direccion=datos['direccion'],
                                zona=datos['zona'],
                                codigo_postal=datos['codigo_postal'],
                                ciudad=datos['ciudad'],
                                departamento=datos['departamento'],
                                pais=datos['pais']
                            )
            db.session.add(proveedor_wms)
            db.session.commit()
        db.session.close()

def cliente_func(filename_input):
    db.session.query(Cliente).delete()
    with open(filename_input, 'r') as file_input:
        input_data = csv.DictReader(file_input, delimiter=';')
        for datos in input_data:
            cliente_wms = Cliente(
                                identificacion=datos['identificacion'], 
                                tipo_identificacion=datos['tipo_identificacion'], 
                                nombre_completo=datos['nombre_completo'], 
                                correo=datos['correo'],
                                telefono=datos['telefono'],
                                celular=datos['celular'],
                                direccion=datos['direccion'],
                                zona=datos['zona'],
                                codigo_postal=datos['codigo_postal'],
                                ciudad=datos['ciudad'],
                                departamento=datos['departamento'],
                                pais=datos['pais']
                            )
            db.session.add(cliente_wms)
            db.session.commit()
        db.session.close()

def producto_func(filename_input):
    db.session.query(Producto).delete()
    with open(filename_input, 'r') as file_input:
        input_data = csv.DictReader(file_input, delimiter=';')
        for datos in input_data:
            producto_wms = Producto(
                                default_code=datos['default_code'], 
                                barcode=datos['barcode'], 
                                name=datos['name'], 
                                categoria=datos['categoria'],
                                precio=datos['precio'],
                                costo=datos['costo'],
                                unidad_venta=datos['unidad_venta'],
                                iva_venta=datos['iva_venta'],
                                volumen=datos['volumen'],
                                peso=datos['peso'],
                                lote=datos['lote'],
                                vence=datos['vence']
                            )
            db.session.add(producto_wms)
            db.session.commit()
        db.session.close()

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    proveedor_func('data/proveedores_wms.csv')
    cliente_func('data/clientes_wms.csv')
    producto_func('data/productos_wms.csv')