# -*- coding : utf-8 -*-
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    tipodocumento = fields.Char(
        string="Tipo documento",
        tracking=True)

    distrito = fields.Char(
        string="distrito",
        tracking=True)

