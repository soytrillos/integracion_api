import xmlrpc.client
import datetime

class maestra_planos:
    def __init__(self, url_rpc, db_rpc, username_rpc, password_rpc):
        self.url_rpc = url_rpc
        self.db_rpc = db_rpc
        self.username_rpc = username_rpc
        self.password_rpc = password_rpc
        
    def cliente_rpc(sefl):
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(sefl.url_rpc))
            uid = common.authenticate(sefl.db_rpc, sefl.username_rpc, sefl.password_rpc, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(sefl.url_rpc))
            return models, uid
        except Exception as error:
            return False
        
    def purchase_order_s(self, models, uid):
        now = datetime.datetime.utcnow()
        filtro = now - datetime.timedelta(days=3)
        filtro = filtro.strftime('%Y-%m-%d')
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'purchase.order', 'search_read', 
            [
                [
                    ['state', '=', 'purchase'],
                    ['invoice_status', '=', 'to invoice'],
                    ['effective_date', '>=', filtro]
                ]
            ], {'fields': ['id', 'name', 'partner_id', 'partner_ref', 'date_approve', 'incoming_picking_count', 'picking_type_id', 'company_id'], 'order': 'id ASC'}
        )        
        return result

    def purchase_order_line_s(self, models, uid, order_id):
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'purchase.order.line', 'search_read', 
            [
                [
                    ['order_id', '=', order_id],
                    ['state', '=', 'purchase']
                ]
            ], {'fields': ['order_id', 'product_id', 'product_qty', 'qty_received', 'taxes_id', 'price_unit', 'company_id']}
        )        
        return result