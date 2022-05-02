# -*- coding: utf-8 -*-
import xmlrpc.client
import datetime

class maestro_transacciones:
    def __init__(self, url_rpc, db_rpc, username_rpc, password_rpc):
        self.url_rpc = url_rpc
        self.db_rpc = db_rpc
        self.username_rpc = username_rpc
        self.password_rpc = password_rpc

    def conexion_rpc(sefl):
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(sefl.url_rpc))
            uid = common.authenticate(sefl.db_rpc, sefl.username_rpc, sefl.password_rpc, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(sefl.url_rpc))
            return models, uid
        except Exception as error:
            return False

    def schema_rpc(self, models, uid, modelo_search):
        
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc,
            modelo_search, 'fields_get', 
                [], 
                {'attributes': ['string', 'help', 'type']})
        return result

    def create_min_max(self, models, uid, datos):
        matriz_error = {}
        matriz_error = []

        producto_result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'product.template', 'search_read', 
            [
                [
                    ['default_code', '=', datos['producto']]
                ]
            ], {'fields': ['id', 'name', 'default_code', 'uom_id', 'categ_id']}
        )
        if producto_result == []:
            matriz_error.append({'error_producto': f'Producto {datos["producto"]} No existe'})
        else:
            consult_p = producto_result[0]
            producto = consult_p['id']
            unidad = consult_p['uom_id']

            minmax_result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.warehouse.orderpoint', 'search_read', 
                [
                    [
                        ['product_id', '=', producto]
                    ]
                ], {'fields': ['id', 'location_id', 'product_min_qty', 'product_max_qty', 'product_uom_name']}
            )
            if minmax_result == []:
                result = models.execute_kw(self.db_rpc, uid, self.password_rpc,
                    'stock.warehouse.orderpoint', 'create', 
                    [
                        {
                            "product_id": producto,
                            "location_id": 8,
                            "product_min_qty": datos["product_min_qty"],
                            "product_max_qty": datos["product_max_qty"],
                            "qty_multiple": datos["qty_multiple"],
                            "product_uom_name": unidad
                        }
                    ]
                )
                return f'Creado correctamente, id: {result}'
            else:
                result = models.execute_kw(self.db_rpc, uid, self.password_rpc,
                    'stock.warehouse.orderpoint', 'write', 
                    [[minmax_result[0]['id']],
                        {
                            "product_id": producto,
                            "location_id": 8,
                            "product_min_qty": datos["product_min_qty"],
                            "product_max_qty": datos["product_max_qty"],
                            "qty_multiple": datos["qty_multiple"],
                            "product_uom_name": unidad
                        }
                    ]
                )
                return f'Actualizado correctamente, {result}'


        if matriz_error != []:
           return matriz_error

    def actualizar_cantidad(self, models, uid, datos):
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc,
            'stock.quant', 'create', 
            [
                {
                    "product_id": int(datos["product_id"]),
                    "location_id": int(datos["location_id"]),
                    "quantity": int(datos["quantity"]),
                    "available_quantity": int(datos["available_quantity"]),
                    "inventory_quantity": int(datos["inventory_quantity"])
                }
            ]
        )
        return result

    def supplier_product(self, models, uid, datos):
        matriz_error = {}
        matriz_error = []

        """
            Validar producto
        """
        producto_result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'product.template', 'search_read', 
            [
                [
                    ['default_code', '=', datos['producto']]
                ]
            ], {'fields': ['id', 'name', 'default_code', 'uom_id', 'categ_id']}
        )
        if producto_result == []:
            matriz_error.append({'error_producto': f'Producto {datos["producto"]} No existe'})
        else:
            consult_p = producto_result[0]
            producto = consult_p['id']

        """
            Validacion contacto
        """
        contacto_resul = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.partner', 'search_read', 
            [
                [
                    ['vat', '=', datos['proveedor']]
                ]
            ], {'fields': ['id', 'vat', 'name']}
        )
        if contacto_resul == []:
            matriz_error.append({'error_contacto': f'Contacto {datos["proveedor"]} No existe'})
        else:
            contacto_resul = contacto_resul[0]
            contacto = contacto_resul['id']

        if matriz_error == []:
            result = models.execute_kw(self.db_rpc, uid, self.password_rpc,
                'product.supplierinfo', 'create', 
                [
                    {
                        "product_tmpl_id": producto,
                        "min_qty": datos["cantidad"],
                        "price": datos["costo"],
                        "delay": datos["plazo_entrega"],
                        "name": contacto
                    }
                ]
            )
            return f'Proveedor Asignado correctamente, id: {result}'
        else:
            return matriz_error

    def transferencias_internas_s(self, models, uid):
        now = datetime.datetime.utcnow()
        filtro = now - datetime.timedelta(days=3)
        filtro = filtro.strftime('%Y-%m-%d')
        print(filtro)
        datos_dict = {}
        cabecera = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.picking', 'search_read', 
            [
                [
                    ['state', '=', 'done'],
                    ['picking_type_id', '=', 5],
                    ['date_done', '>=', f"'{filtro}'"]
                ]
            ], {'fields': ['id', 'name', 'origin', 'state', 'partner_id', 'note', 'date_done', 'location_id', 'location_dest_id', 'picking_type_id'], 'order': 'id ASC'}
        )

        for consult_c in cabecera:
            datos_dict[consult_c['name']] = []
            
            if consult_c['partner_id'] != False:
                partner = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                    'res.partner', 'search_read', 
                    [
                        [
                            ['id', '=', consult_c['partner_id'][0]]
                        ]
                    ], {'fields': ['vat', 'name']}
                )
                partner = partner[0]['vat']
            else:
                partner = False

            location_source = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.location', 'search_read', 
                [
                    [
                        ['id', '=', consult_c['location_id'][0]]
                    ]
                ], {'fields': ['complete_name', 'name', 'display_name', 'comment']}
            )
            location_source = str(location_source[0]['comment']).replace('<p>', '').replace('</p>', '')

            location_dest = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.location', 'search_read', 
                [
                    [
                        ['id', '=', consult_c['location_dest_id'][0]]
                    ]
                ], {'fields': ['complete_name', 'name', 'display_name', 'comment']}
            )
            location_dest = str(location_dest[0]['comment']).replace('<p>', '').replace('</p>', '')

            datos_dict[consult_c['name']] = {
                'id': consult_c['id'],
                'name': consult_c['name'],
                'origin': consult_c['origin'],
                'state': consult_c['state'],
                'partner_id': partner,
                'date_done': consult_c['date_done'],
                'location_source': location_source,
                'location_dest': location_dest,
                'observation': str(consult_c['note']).replace('<p>', '').replace('</p>', '')
            }

            datos_dict[consult_c['name']]['detalle'] = []

            detalle = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.move.line', 'search_read', 
                [
                    [
                        ['picking_id', '=', consult_c['id']]
                    ]
                ], {'fields': ['product_id', 'product_qty', 'qty_done', 'lot_id', 'lot_name', 'picking_code']}
            )

            for consult_d in detalle:
                producto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                    'product.template', 'search_read', 
                    [
                        [
                            ['id', '=', consult_d['product_id'][0]]
                        ]
                    ], {'fields': ['id', 'name', 'default_code']}
                )
                producto = producto[0]['default_code']

                datos_dict[consult_c['name']]['detalle'].append({
                    'product_id': producto,
                    'qty_done': consult_d['qty_done'],
                    'lot_id': consult_d['lot_id'],
                    'lot_name': consult_d['lot_name']
                })

        return datos_dict

    def transferencias_internas_c(self, models, uid, datos):
        matriz_error = {}
        matriz_error = []

        """
            Validar documento
        """
        validacion_documento = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.picking', 'search_read', 
            [
                [
                    ['name', '=', datos['name']]
                ]
            ], {'fields': ['id', 'name']}
        )
        if validacion_documento != []:
            matriz_error.append({'error_documento': f'Documento {datos["name"]} ya existe'})

        """
            Validacion contacto
        """
        contacto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.partner', 'search_read', 
            [
                [
                    ['vat', '=', datos['partner_id']]
                ]
            ], {'fields': ['id', 'vat', 'name']}
        )
        if contacto == []:
            matriz_error.append({'error_contacto': f'Contacto {datos["partner_id"]} No existe'})
        else:
            contacto = contacto[0]['id']

        """
            Validar ubicaciones
        """
        location_source = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.location', 'search_read', 
            [
                [
                    ['comment', 'like', f"%{datos['location_id']}%"]
                ]
            ], {'fields': ['complete_name', 'name', 'display_name', 'comment']}
        )
        if location_source == []:
            matriz_error.append({'error_ubicacion_fuente': f'Ubicacion {datos["location_id"]} No existe'})
        else:
            location_source = int(location_source[0]['id'])

        location_dest = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.location', 'search_read', 
            [
                [
                    ['comment', 'like', f"%{datos['location_dest_id']}%"]
                ]
            ], {'fields': ['complete_name', 'name', 'display_name', 'comment']}
        )
        if location_dest == []:
            matriz_error.append({'error_ubicacion_destino': f'Ubicacion {datos["location_dest_id"]} No existe'})
        else:
            location_dest = int(location_dest[0]['id'])

        """
            Validar producto antes de insertar
        """
        for prod in datos['detalle']:
            producto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'product.template', 'search_read', 
                [
                    [
                        ['default_code', '=', prod['producto']]
                    ]
                ], {'fields': ['id', 'name', 'default_code', 'uom_id']}
            )
            if producto == []:
                matriz_error.append({'error_producto': f'Producto {prod["producto"]} No existe'})
            else:
                consult_p = producto[0]

        

        if matriz_error == []:
            encabezado = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.picking', 'create', 
                [
                    {
                        
                        "name": datos['name'],
                        "origin": datos['origin'],
                        "partner_id": contacto, # Validar que exista
                        "location_id": location_source, # Validar que exista
                        "location_dest_id": location_dest, # Validar que exista
                        "state": "done",
                        "note": datos['note'],
                        "picking_type_id": 5, # Transferencia interna
                        "show_mark_as_todo": False,
                        "show_operations": True,
                        "show_reserved": True
                    }
                ]
            )

            for datos_d in datos['detalle']:
                """
                    Validar producto
                """
                try:
                    producto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                        'product.template', 'search_read', 
                        [
                            [
                                ['default_code', '=', datos_d['producto']]
                            ]
                        ], {'fields': ['id', 'name', 'default_code', 'uom_id']}
                    )
                    if producto == []:
                        matriz_error.append({'error_producto': f'Producto {datos["product_id"]} No existe'})
                    else:
                        consult_p = producto[0]
                        producto = consult_p['id']
                        unidad = consult_p['uom_id'][0]
                
                    detalle = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                        'stock.move.line', 'create', 
                        [
                            {
                                "picking_id": encabezado,
                                "reference": datos['name'],
                                "state": "done",
                                "product_id": producto,
                                "product_uom_id": 1,
                                "location_id": location_source,
                                "location_dest_id": location_dest,
                                "product_uom_id": unidad,
                                "qty_done": datos_d['cantidad'],
                                "picking_code": 5
                            }
                        ]
                    )
                except Exception as error:
                    matriz_error.append({'error_creando': f'Error al intentar crear documento {error}'})

            if matriz_error != []:
                eliminar_encabezado = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                    'stock.picking', 'unlink', 
                    [[encabezado]]
                )
                return matriz_error
            else:
                return f'Creado correctamente, se debe terminar de aprobar en web id: {encabezado}'
        else:
            return matriz_error

    def devolucion_mercancia_s(self, models, uid):
        """
            Localizaciones destino para devoluciones
                - id: 5, Clientes - Customers
                - id: 4, Proveedores - Vendors
        """
        datos_dict = {}
        cabecera = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.picking', 'search_read', 
            [
                [
                    ['state', '=', 'done'],
                    ['picking_type_id', '=', 6]
                ]
            ], {'fields': ['id', 'name', 'origin', 'state', 'partner_id', 'note', 'date_done', 'location_id', 'location_dest_id', 'picking_type_id']}
        )

        for consult_c in cabecera:
            datos_dict[consult_c['name']] = []
            
            partner = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'res.partner', 'search_read', 
                [
                    [
                        ['id', '=', consult_c['partner_id'][0]]
                    ]
                ], {'fields': ['vat', 'name']}
            )
            partner = partner[0]['vat']

            location_source = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.location', 'search_read', 
                [
                    [
                        ['id', '=', consult_c['location_id'][0]]
                    ]
                ], {'fields': ['complete_name', 'name', 'display_name', 'comment']}
            )
            location_source = str(location_source[0]['comment']).replace('<p>', '').replace('</p>', '')

            location_dest = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.location', 'search_read', 
                [
                    [
                        ['id', '=', consult_c['location_dest_id'][0]]
                    ]
                ], {'fields': ['complete_name', 'name', 'display_name', 'comment']}
            )
            location_dest = str(location_dest[0]['comment']).replace('<p>', '').replace('</p>', '')

            datos_dict[consult_c['name']] = {
                'id': consult_c['id'],
                'name': consult_c['name'],
                'origin': consult_c['origin'],
                'state': consult_c['state'],
                'partner_id': partner,
                'date_done': consult_c['date_done'],
                'location_source': location_source,
                'location_dest': location_dest,
                'observation': str(consult_c['note']).replace('<p>', '').replace('</p>', '')
            }

            datos_dict[consult_c['name']]['detalle'] = []

            detalle = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.move.line', 'search_read', 
                [
                    [
                        ['picking_id', '=', consult_c['id']]
                    ]
                ], {'fields': ['product_id', 'product_qty', 'qty_done', 'lot_id', 'lot_name', 'picking_code']}
            )

            for consult_d in detalle:
                producto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                    'product.template', 'search_read', 
                    [
                        [
                            ['id', '=', consult_d['product_id'][0]]
                        ]
                    ], {'fields': ['id', 'name', 'default_code']}
                )
                producto = producto[0]['default_code']

                datos_dict[consult_c['name']]['detalle'].append({
                    'product_id': producto,
                    'qty_done': consult_d['qty_done'],
                    'lot_id': consult_d['lot_id'],
                    'lot_name': consult_d['lot_name']
                })

        return datos_dict

    def devolucion_mercancia_c(self, models, uid, datos):
        """
            Localizaciones destino para devoluciones
                - id: 5, Clientes - Customers
                - id: 4, Proveedores - Vendors
        """
        matriz_error = {}
        matriz_error = []

        """
            Validar documento
        """
        validacion_documento = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.picking', 'search_read', 
            [
                [
                    ['name', '=', datos['name']]
                ]
            ], {'fields': ['id', 'name']}
        )
        if validacion_documento != []:
            matriz_error.append({'error_documento': f'Documento {datos["name"]} ya existe'})

        """
            Validacion contacto
        """
        contacto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.partner', 'search_read', 
            [
                [
                    ['vat', '=', datos['partner_id']]
                ]
            ], {'fields': ['id', 'vat', 'name']}
        )
        if contacto == []:
            matriz_error.append({'error_contacto': f'Contacto {datos["partner_id"]} No existe'})
        else:
            contacto = contacto[0]['id']

        """
            Validar ubicaciones
        """

        if datos['type_return'] == 'Cliente':
            location_source = 5
            location_dest = 8
        elif datos['type_return'] == 'Proveedor':
            location_dest = 4
            location_source = 8
        else:
            matriz_error.append({'error_tipo_devolucion': f"Solo se permiten devoluciones 'Cliente' o 'Proveedor', parametro {datos['type_return']} incorrecto"})


        """
            Validar productos antes de insertar
        """
        for prod in datos['detalle']:
            producto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'product.template', 'search_read', 
                [
                    [
                        ['default_code', '=', prod['producto']]
                    ]
                ], {'fields': ['id', 'name', 'default_code', 'uom_id']}
            )
            if producto == []:
                matriz_error.append({'error_producto': f'Producto {prod["producto"]} No existe'})
            else:
                consult_p = producto[0]

        
        if matriz_error == []:
            encabezado = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.picking', 'create', 
                [
                    {
                        
                        "name": datos['name'],
                        "origin": datos['origin'],
                        "partner_id": contacto, # Validar que exista
                        "location_id": location_source, # Validar que exista
                        "location_dest_id": location_dest, # Validar que exista
                        "state": "done",
                        "note": datos['note'],
                        "picking_type_id": 6, # Transferencia interna
                        "show_mark_as_todo": False,
                        "show_operations": True,
                        "show_reserved": True
                    }
                ]
            )

            for datos_d in datos['detalle']:
                """
                    Validar producto
                """
                try:
                    producto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                        'product.template', 'search_read', 
                        [
                            [
                                ['default_code', '=', datos_d['producto']]
                            ]
                        ], {'fields': ['id', 'name', 'default_code', 'uom_id']}
                    )
                    if producto == []:
                        matriz_error.append({'error_producto': f'Producto {datos["product_id"]} No existe'})
                    else:
                        consult_p = producto[0]
                        producto = consult_p['id']
                        unidad = consult_p['uom_id'][0]

                    detalle = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                        'stock.move.line', 'create', 
                        [
                            {
                                "picking_id": encabezado,
                                "reference": datos['name'],
                                "state": "done",
                                "product_id": producto,
                                "product_uom_id": 1,
                                "location_id": location_source,
                                "location_dest_id": location_dest,
                                "product_uom_id": unidad,
                                "qty_done": datos_d['cantidad'],
                                "picking_code": 6
                            }
                        ]
                    )
                except Exception as error:
                    matriz_error.append({'error_creando': f'Error al intentar crear documento {error}'})

            if matriz_error != []:
                eliminar_encabezado = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                    'stock.picking', 'unlink', 
                    [[encabezado]]
                )
                return matriz_error
            else:
                return f'Creado correctamente, se debe confirmar en la web, id: {encabezado}'
        else:
            return matriz_error

    def ajuste_inventario_s(self, models, uid, datos):
        datos_dict = {}
        ajustes = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.quant', 'search_read', 
            [
                [
                    ['quantity', '>', 0],
                    ['available_quantity', '>', 0]
                ]
            ], {'fields': ['id', 'product_id', 'product_uom_id', 'location_id', 'lot_id', 'package_id', 'quantity', 'reserved_quantity', 'available_quantity', 'on_hand', 'inventory_quantity_set']}
        )

        count = 1
        for consult_s in ajustes:
            datos_dict[f'Ajuste-{count}'] = []

            location_source = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.location', 'search_read', 
                [
                    [
                        ['id', '=', consult_s['location_id'][0]]
                    ]
                ], {'fields': ['complete_name', 'name', 'display_name', 'comment']}
            )
            location_source = str(location_source[0]['comment']).replace('<p>', '').replace('</p>', '')

            producto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'product.template', 'search_read', 
                [
                    [
                        ['id', '=', consult_s['product_id'][0]]
                    ]
                ], {'fields': ['id', 'name', 'default_code', 'uom_id']}
            )
            producto = producto[0]['default_code']

            datos_dict[f'Ajuste-{count}'] = {
                'product_id': producto,
                'product_uom_id': consult_s['product_uom_id'][1],
                'location_id': location_source,
                'lot_id': consult_s['lot_id'],
                'package_id': consult_s['package_id'],
                'quantity': consult_s['quantity'],
                'reserved_quantity': consult_s['reserved_quantity'],
                'available_quantity': consult_s['available_quantity']
            }
            count += 1

        return datos_dict

    def ajuste_inventario_c(self, models, uid, datos):
        matriz_error = {}

        """
            Validacion producto
        """
        producto_result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'product.template', 'search_read', 
            [
                [
                    ['default_code', '=', datos['product_id']]
                ]
            ], {'fields': ['id', 'name', 'default_code', 'uom_id']}
        )
        if producto_result != []:
            producto_result = producto_result[0]
            producto = producto_result['id']
            unidad_medida = producto_result['uom_id']
        else:
            matriz_error = {'error_producto': f'El producto {datos["product_id"]}'}

        """
            Validacion localizacion
        """
        location_id = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.location', 'search_read', 
            [
                [
                    ['comment', 'like', f"%{datos['location_id']}%"]
                ]
            ], {'fields': ['complete_name', 'name', 'display_name', 'comment']}
        )
        location_id = location_id[0]['id']

        """
            Validacion inventario de producto y localizacion
        """
        ajustes = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'stock.quant', 'search_read', 
            [
                [
                    ['product_id', '=', producto],
                    ['location_id', '=', location_id]
                ]
            ], {'fields': ['id']}
        )
        if ajustes == []:
            ajuste = 0
        else:
            ajuste = ajustes[0]['id']

        if matriz_error == {} and ajuste != 0:
            ajuste = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.quant', 'write', 
                [
                    [ajuste],
                    {
                        'product_id': producto,
                        'product_uom_id': unidad_medida,
                        'location_id': location_id,
                        'lot_id': datos['lot_id'],
                        'package_id': datos['package_id'],
                        'quantity': datos['quantity'],
                        'inventory_quantity': datos['inventory_quantity'],
                        'inventory_diff_quantity': 0
                    }
                ]
            )
            return f'Creado correctamente {ajuste}'
        else:
            return matriz_error
