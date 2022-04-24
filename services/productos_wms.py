import xmlrpc.client

class maestra_productos:
    def __init__(self, url_rpc, db_rpc, username_rpc, password_rpc):
        self.url_rpc = url_rpc
        self.db_rpc = db_rpc
        self.username_rpc = username_rpc
        self.password_rpc = password_rpc

    def cliente_rpc(sefl):
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(sefl.url_rpc))
        uid = common.authenticate(sefl.db_rpc, sefl.username_rpc, sefl.password_rpc, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(sefl.url_rpc))
        return models, uid

    def consulta_producto(self, models, uid, cod_product):
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'product.template', 'search_read', 
            [
                [
                    ['default_code', '=', cod_product]
                ]
            ], {'fields': ['id', 'name']}
        )        
        return result

    def crear_producto(self, models, uid, datos):
        matrix_result = {}
        matrix_result['resultado'] = []
        """
            Validacion y creacion de la categoria
        """
        s_categoria = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'product.category', 'search_read', 
            [
                [
                    ['name', '=', datos['categoria']]
                ]
            ], {'fields': ['id']}
        )
        if s_categoria == []:
            s_categoria = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'product.category', 'create', 
                [
                    {
                        'name': str(datos['categoria'])
                    }
                ]
            )
        else:
            s_categoria = s_categoria[0]['id']

        """
            Validacion y asignacion de ID de Unidad de medida
        """
        s_unidad = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'uom.uom', 'search_read', 
            [
                [
                    ['name', '=', datos['unidad_venta']]
                ]
            ], {'fields': ['id']}
        )
        if s_unidad == []:
            matrix_result['resultado'].append({'error_unidad': f'La unidad de medida: {datos["unidad_venta"]}, no existe'})
        else:
            s_unidad = s_unidad[0]['id']

        """
            Validacion impuesto
        """
        s_impuesto_sale = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'account.tax', 'search_read', 
            [
                [
                    ['amount', '=', datos["iva_venta"]],
                    ['type_tax_use', '=', 'sale'],
                    ['amount_type', '=', 'percent']
                ]
            ], {'fields': ['id']}
        )
        if s_impuesto_sale != []:
            s_impuesto_sale = s_impuesto_sale[0]['id']
        else:
            matrix_result['resultado'].append({'error_impuesto': f'El impuesto {datos["iva_venta"]}, no existe'})
        
        s_impuesto_purchase = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'account.tax', 'search_read', 
            [
                [
                    ['amount', '=', datos["iva_venta"]],
                    ['type_tax_use', '=', 'purchase'],
                    ['amount_type', '=', 'percent']
                ]
            ], {'fields': ['id']}
        )
        if s_impuesto_purchase != []:
            s_impuesto_purchase = s_impuesto_purchase[0]['id']
        else:
            matrix_result['resultado'].append({'error_impuesto': f'El impuesto {datos["iva_venta"]}, no existe'})


        if matrix_result == {'resultado': []}:
            result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'product.template', 'create', 
                [
                    {
                        "default_code": str(datos["default_code"]),
                        "barcode": str(datos["barcode"]),
                        "name": str(datos["name"]),
                        "categ_id": int(s_categoria),
                        "price": str(datos["precio"]),
                        "standard_price": str(datos["costo"]),
                        "uom_id": int(s_unidad),
                        "uom_po_id": int(s_unidad),
                        "taxes_id": [int(s_impuesto_sale)],
                        "supplier_taxes_id": [int(s_impuesto_purchase)],
                        "type": str(datos["tipo_producto"]),
                        "volume": str(datos["volumen"]),
                        "weight": str(datos["peso"]),
                        "active": 1
                    }
                ]
            )
            matrix_result['resultado'].append({'id_producto': f'{result} - {datos["name"]}'})
        return matrix_result


    def actualizar_producto(self, models, uid, datos, id_product):
        matrix_result = {}
        matrix_result['resultado'] = []
        """
            Validacion y creacion de la categoria
        """
        s_categoria = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'product.category', 'search_read', 
            [
                [
                    ['name', '=', datos['categoria']]
                ]
            ], {'fields': ['id']}
        )
        if s_categoria == []:
            s_categoria = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'product.category', 'create', 
                [
                    {
                        'name': str(datos['categoria'])
                    }
                ]
            )
        else:
            s_categoria = s_categoria[0]['id']

        """
            Validacion y asignacion de ID de Unidad de medida
        """
        s_unidad = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'uom.uom', 'search_read', 
            [
                [
                    ['name', '=', datos['unidad_venta']]
                ]
            ], {'fields': ['id']}
        )
        if s_unidad == []:
            matrix_result['resultado'].append({'error_unidad': f'La unidad de medida: {datos["unidad_venta"]}, no existe'})
        else:
            s_unidad = s_unidad[0]['id']

        """
            Validacion impuesto
        """
        s_impuesto_sale = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'account.tax', 'search_read', 
            [
                [
                    ['amount', '=', datos["iva_venta"]],
                    ['type_tax_use', '=', 'sale'],
                    ['amount_type', '=', 'percent']
                ]
            ], {'fields': ['id']}
        )
        if s_impuesto_sale != []:
            s_impuesto_sale = s_impuesto_sale[0]['id']
        else:
            matrix_result['resultado'].append({'error_impuesto': f'El impuesto {datos["iva_venta"]}, no existe'})
        
        s_impuesto_purchase = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'account.tax', 'search_read', 
            [
                [
                    ['amount', '=', datos["iva_venta"]],
                    ['type_tax_use', '=', 'purchase'],
                    ['amount_type', '=', 'percent']
                ]
            ], {'fields': ['id']}
        )
        if s_impuesto_purchase != []:
            s_impuesto_purchase = s_impuesto_purchase[0]['id']
        else:
            matrix_result['resultado'].append({'error_impuesto': f'El impuesto {datos["iva_venta"]}, no existe'})
        
        if matrix_result == {'resultado': []}:
            try:
                result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                    'product.template', 'write', 
                    [
                        [id_product], 
                        {
                            "default_code": str(datos["default_code"]),
                            "barcode": str(datos["barcode"]),
                            "name": str(datos["name"]),
                            "categ_id": int(s_categoria),
                            "price": str(datos["precio"]),
                            "standard_price": str(datos["costo"]),
                            "uom_id": int(s_unidad),
                            "uom_po_id": int(s_unidad),
                            "taxes_id": [int(s_impuesto_sale)],
                            "supplier_taxes_id": [int(s_impuesto_purchase)],
                            "type": str(datos["tipo_producto"]),
                            "volume": str(datos["volumen"]),
                            "weight": str(datos["peso"])
                        }
                    ]
                )
                matrix_result['resultado'].append({'cod_producto': f'{id_product} - {datos["name"]}', 'code': result})
            except Exception as error:
                print(f'Error: {error.args}')
        return matrix_result