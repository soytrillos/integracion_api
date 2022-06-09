import xmlrpc.client

class maestra_parametros:
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
        
    def creacion_localizacion(self, models, uid, datos):
        resultado = []
        for dato in datos['localizaciones']:
            localizacion_padre = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.location', 'search_read', 
                [
                    [
                        ['complete_name', '=', "WH/Stock"]
                    ]
                ], {'fields': ['id', 'name']}
            )
            if localizacion_padre != []:
                padre = localizacion_padre[0]['id']
            else:
                padre = 0
            
            busqueda_localizacion = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'stock.location', 'search_read', 
                [
                    [
                        ['complete_name', '=', f"WH/Stock/{dato['name']}"]
                    ]
                ], {'fields': ['id', 'name']}
            )
            
            if busqueda_localizacion == []:
                creacion_localizacion = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                    'stock.location', 'create', 
                    [
                        {
                            "location_id": padre,
                            "complete_name": f"WH/Stock/{dato['name']}",
                            "name": dato['name']
                        }
                    ]
                )
                resultado.append({'Localizacion': dato['name'], 'Id': creacion_localizacion})
            else:
                resultado.append({'Localizacion': dato['name'], 'Id': 'Ya existe'})
            
        return resultado