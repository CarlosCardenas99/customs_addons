# -*- coding: utf-8 -*-
{
    'name': "POS Company Logo",
    'summary': """This module shows company logo in the POS header""",
    'author': "Brent137",
    'website': "https://github.com/brent137",
    'category': 'Sales/Point of Sale',
    'version': '16.0.0',
    'depends': ['point_of_sale'],
    'data': [

    ],
    'assets': {
        'point_of_sale.assets': [
            'b1_pos_company_logo/static/src/css/company_logo.scss',
            'b1_pos_company_logo/static/src/js/**/*.js',
            'b1_pos_company_logo/static/src/xml/**/*',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
}
