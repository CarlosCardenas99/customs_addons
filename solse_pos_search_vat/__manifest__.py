# -*- coding: utf-8 -*-
# Copyright (c) 2019-2022 Juan Gabriel Fernandez More (kiyoshi.gf@gmail.com)
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

{
	'name': "Búsqueda RUC/DNI desde POS",

	'summary': """
		Obtener datos con RUC o DNI desde POS
		""",

	'description': """
		Obtener los datos por RUC o DNI desde POS
	""",

	'author': "F & M Solutions Service S.A.C",
	'website': "http://www.solse.pe",

	'category': 'Uncategorized',
	'version': '16.0.0.1',
	'license': 'Other proprietary',
	'depends': ['l10n_pe', 'l10n_latam_base', 'point_of_sale'],

	'data': [],
	'assets': {
		'point_of_sale.assets': [
			'/solse_pos_search_vat/static/src/js/PartnerListScreen.js',
		],
	},
	'demo': [],
	'installable': True,
	'auto_install': False,
	'application': True,
	"sequence": 1,
}