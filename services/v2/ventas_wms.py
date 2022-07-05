# -*- coding: utf-8 -*-
import xmlrpc.client

class maestro_ventas:
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
    
    def productos_rpc(self, models, uid, id_producto):
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'product.product', 'search_read', 
            [
                [
                    ['id', '=', id_producto]
                ]
            ], {'fields': ['id', 'name', 'default_code']}
        )        
        return result

    def iva_rpc(self, models, uid, id_iva):
        s_impuesto_sale = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'account.tax', 'search_read', 
            [
                [
                    ['id', '=', id_iva],
                    ['type_tax_use', '=', 'sale'],
                    ['amount_type', '=', 'percent']
                ]
            ], {'fields': ['id', 'amount']}
        )
        return s_impuesto_sale

    def clientes_rpc(self, models, uid, id_cliente):
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.partner', 'search_read', 
            [
                [
                    ['id', '=', id_cliente]
                ]
            ], {'fields': ['id', 'vat', 'name']}
        )        
        return result

    def sale_order_s(self, models, uid):
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'sale.order', 'search_read', 
            [
                [
                    ['state', '=', 'sale'],
                    ['invoice_status', '=', 'to invoice'],
                    ['date_order', '>=', '2022-04-24']
                ]
            ], {'fields': ['id', 'name', 'partner_id', 'date_order', 'delivery_count', 'company_id', 'warehouse_id'], 'order': 'id ASC'}
        )        
        return result

    def sale_order_line_s(self, models, uid, order_id):
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'sale.order.line', 'search_read', 
            [
                [
                    ['order_id', '=', order_id],
                    ['state', '=', 'sale']
                ]
            ], {'fields': ['order_id', 'product_id', 'product_uom_qty', 'tax_id', 'price_unit', 'discount']}
        )        
        return result
    
    def validacion_documento(self, models, uid, datos):
        resultados = {}
        validacion_documento = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'sale.order', 'search_read', 
            [
                [
                    ['name', '=', datos['name']]
                ]
            ], {'fields': ['id', 'name']}
        )
        resultados = {'documento': validacion_documento}
        return resultados


    def sale_order_c(self, models, uid, datos, id_cliente):
        encabezado = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'sale.order', 'create', 
            [
                {
                    "name": str(datos["name"]),
                    "partner_id": int(id_cliente),
                    "date_order": str(datos["date_order"]),
                    "state": "sale"
                }
            ]
        )
        return encabezado

    def iva_producto(self, models, uid, impuesto):
        """
            Validacion impuesto
        """
        s_impuesto_sale = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'account.tax', 'search_read', 
            [
                [
                    ['amount', '=', impuesto],
                    ['type_tax_use', '=', 'sale'],
                    ['amount_type', '=', 'percent']
                ]
            ], {'fields': ['id']}
        )
        if s_impuesto_sale != []:
            return s_impuesto_sale
        else:
            s_impuesto_sale = []
            return s_impuesto_sale
    
    def sale_order_line_c(self, models, uid, datos, encabezado, id_producto):
        producto = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'product.product', 'search_read', 
            [
                [
                    ['default_code', '=', id_producto]
                ]
            ], {'fields': ['id', 'name']}
        )
        """
            Validacion impuesto
        """
        s_impuesto_sale = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'account.tax', 'search_read', 
            [
                [
                    ['amount', '=', datos['tax_id']],
                    ['type_tax_use', '=', 'sale'],
                    ['amount_type', '=', 'percent']
                ]
            ], {'fields': ['id']}
        )
        if s_impuesto_sale != []:
            s_impuesto_sale = s_impuesto_sale[0]['id']
            detalle = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'sale.order.line', 'create', 
                [
                    {
                        "order_id": int(encabezado),
                        "product_id": int(producto[0]['id']),
                        "product_uom_qty": float(datos["product_uom_qty"]),
                        "tax_id": [int(s_impuesto_sale)],
                        "price_unit": float(datos["price_unit"]),
                        "discount": float(datos["discount"])
                    }
                ]
            )
            return detalle
        else:
            return 'Inconveniente impuesto'
