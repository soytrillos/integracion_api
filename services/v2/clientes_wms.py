# -*- coding: utf-8 -*-
import xmlrpc.client

class maestra_clientes:
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

    def consulta_cliente(self, models, uid, nit_cliente):
        result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.partner', 'search_read', 
            [
                [
                    ['vat', '=', nit_cliente]
                ]
            ], {'fields': ['id', 'name', 'vat']}
        )        
        return result
    
    def crear_cliente(self, models, uid, datos):
        matrix_result = {}
        matrix_result['resultado'] = []
        """
            Validacion tipo de identificacion
        """
        s_identificacion = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'l10n_latam.identification.type', 'search_read', 
            [
                [
                    ['name', '=', datos['tipo_identificacion']]
                ]
            ], {'fields': ['id']}
        )
        
        if s_identificacion == []:
            identificaciones = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'l10n_latam.identification.type', 'search_read', 
                [], 
                {'fields': ['id', 'name']}
            )
            matrix_result['resultado'].append({'error_identificacion': f'El tipo de identificacion: {datos["tipo_identificacion"]}, no existe o esta incompleto', 'permitidos': identificaciones}) 
        else:
            s_identificacion = s_identificacion[0]['id']

        """
            Validar o crear Zona
        """
        # Busca
        zona = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'partner.delivery.zone', 'search_read', 
            [
                [
                    ['name', '=', datos["zona"]]
                ]
            ], {'fields': ['name']}
        )

        if zona == []:
            zona = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'partner.delivery.zone', 'create', 
                [
                    {
                        'code': datos["zona"],
                        'name': datos["zona"]
                    }
                ]
            )
        else:
            zona = zona[0]['id']

        """
            Validacion pais 
        """
        s_pais = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.country', 'search_read', 
            [
                [
                    ['name', '=', datos['pais'].capitalize()]
                ]
            ], {'fields': ['id']}
        )
        if s_pais == []:
            s_pais = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'res.country', 'search_read', 
                [
                    [
                        ['name', 'like', datos["pais"].capitalize()]
                    ]
                ], {'fields': ['name']}
            )
            if s_pais == []:
                matrix_result['resultado'].append({'error_pais': f'El pais {datos["pais"]}, no existe o esta mal', 'semejanzas': 'No se encontraron'})
            else:
                matrix_result['resultado'].append({'error_pais': f'El pais {datos["pais"]}, no existe o esta mal', 'semejanzas': s_pais[0]["name"] })
        else:
            s_pais = s_pais[0]['id']

        """
            Validacion departamento
        """
        s_departamento = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.country.state', 'search_read', 
            [
                [
                    ['name', '=', datos["departamento"].capitalize()]
                ]
            ], {'fields': ['id']}
        )
        if s_departamento == []:
            s_departamento = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'res.country', 'search_read', 
                [
                    [
                        ['name', 'like', datos["departamento"].capitalize()]
                    ]
                ], {'fields': ['name']}
            )
            if s_departamento == []:
                matrix_result['resultado'].append({'error_departamento': f'El departamento {datos["departamento"]}, no existe o esta mal', 'semejanzas': 'No se encontraron'})
            else:
                matrix_result['resultado'].append({'error_departamento': f'El departamento {datos["departamento"]}, no existe o esta mal', 'semejanzas': s_departamento[0]["name"] })
        else:
            s_departamento = s_departamento[0]['id']

        if matrix_result == {'resultado': []}:
            result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'res.partner', 'create', 
                [
                    {
                        'vat': datos["vat"],
                        'l10n_latam_identification_type_id': int(s_identificacion),
                        'name': datos["nombre_completo"],
                        'email': datos["correo"],
                        'phone': datos["telefono"],
                        'mobile': datos["celular"],
                        'street': datos["direccion"],
                        'delivery_zone_id': zona,
                        'zip': datos["codigo_postal"],
                        'city': datos["ciudad"],
                        'state_id': int(s_departamento),
                        'country_id': int(s_pais),
                        'customer_rank': 1
                    }
                ]
            )
            matrix_result['resultado'].append({'id_cliente': f'{result} - {datos["nombre_completo"]}'})
        return matrix_result

    def actualizar_cliente(self, models, uid, datos, id_cliente):
        matrix_result = {}
        matrix_result['resultado'] = []

        """
            Validar o crear Zona
        """
        # Busca
        zona = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'partner.delivery.zone', 'search_read', 
            [
                [
                    ['name', '=', datos["zona"]]
                ]
            ], {'fields': ['name']}
        )

        if zona == []:
            zona = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'partner.delivery.zone', 'create', 
                [
                    {
                        'code': datos["zona"],
                        'name': datos["zona"]
                    }
                ]
            )
        else:
            zona = zona[0]['id']
        
        """
            Validacion pais 
        """
        s_pais = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.country', 'search_read', 
            [
                [
                    ['name', '=', datos["pais"].capitalize()]
                ]
            ], {'fields': ['id']}
        )
        if s_pais == []:
            s_pais = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'res.country', 'search_read', 
                [
                    [
                        ['name', 'like', datos["pais"].capitalize()]
                    ]
                ], {'fields': ['name']}
            )
            if s_pais == []:
                matrix_result['resultado'].append({'error_pais': f'El pais {datos["pais"]}, no existe o esta mal', 'semejanzas': 'No se encontraron'})
            else:
                matrix_result['resultado'].append({'error_pais': f'El pais {datos["pais"]}, no existe o esta mal', 'semejanzas': s_pais[0]["name"] })
        else:
            s_pais = s_pais[0]['id']

        """
            Validacion departamento
        """
        s_departamento = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
            'res.country.state', 'search_read', 
            [
                [
                    ['name', '=', datos["departamento"].capitalize()]
                ]
            ], {'fields': ['id']}
        )
        if s_departamento == []:
            s_departamento = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'res.country', 'search_read', 
                [
                    [
                        ['name', 'like', datos["departamento"].capitalize()]
                    ]
                ], {'fields': ['name']}
            )
            if s_departamento == []:
                matrix_result['resultado'].append({'error_departamento': f'El departamento {datos["departamento"]}, no existe o esta mal', 'semejanzas': 'No se encontraron'})
            else:
                matrix_result['resultado'].append({'error_departamento': f'El departamento {datos["departamento"]}, no existe o esta mal', 'semejanzas': s_departamento[0]["name"] })
        else:
            s_departamento = s_departamento[0]['id']
        
        if matrix_result == {'resultado': []}:
            result = models.execute_kw(self.db_rpc, uid, self.password_rpc, 
                'res.partner', 'write', 
                [
                    [id_cliente],
                    {
                        'name': datos["nombre_completo"],
                        'email': datos["correo"],
                        'phone': datos["telefono"],
                        'mobile': datos["celular"],
                        'street': datos["direccion"],
                        'delivery_zone_id': zona,
                        'zip': datos["codigo_postal"],
                        'city': datos["ciudad"],
                        'state_id': int(s_departamento),
                        'country_id': int(s_pais),
                        'customer_rank': 1
                    }
                ]
            )
            matrix_result['resultado'].append({'id_cliente': f'{id_cliente} - {datos["nombre_completo"]}', 'code': result})
        return matrix_result