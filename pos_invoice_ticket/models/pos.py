from odoo import models, fields


class PosOrder(models.Model):
    _inherit = 'pos.order'

    type_document = fields.Selection(
        selection=[('b', 'Boleta'), ('f', 'Factura')],
        string='Tipo de documento',
        states={'done': [('readonly', True)], 'invoiced': [('readonly', True)]})




