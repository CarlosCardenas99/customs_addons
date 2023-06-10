# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Pos impresión ticket boleta y ticket factura.',
    'version': '10.0',
    'author': 'Bitodoo',
    'category': 'Point of Sale',
    'summary': 'Impresión ticket boleta y ticket factura.',
    'website': 'https://www.bitodoo.com',
    'license': 'AGPL-3',
    'description': """
        Impresión ticket boleta y ticket factura.
    """,
    'depends': ['point_of_sale'],
    'data': [
        'template/template.xml',
        'views/pos.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
}
