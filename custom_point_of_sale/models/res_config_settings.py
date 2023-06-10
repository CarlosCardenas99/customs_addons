# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2019-TODAY OPeru.
#    Author      :  Grupo Odoo S.A.C. (<http://www.operu.pe>)
#
#    This program is copyright property of the author mentioned above.
#    You can`t redistribute it and/or modify it.
#
###############################################################################

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_pe_api_ruc_connection = fields.Selection(related='company_id.l10n_pe_api_ruc_connection', readonly=False)
    l10n_pe_api_dni_connection = fields.Selection(related='company_id.l10n_pe_api_dni_connection', readonly=False)
    l10n_pe_partner_token = fields.Char(related='company_id.l10n_pe_partner_token', readonly=False)
    l10n_pe_ruc_validation = fields.Boolean(related='company_id.l10n_pe_ruc_validation', readonly=False)
    l10n_pe_dni_validation = fields.Boolean(related='company_id.l10n_pe_dni_validation', readonly=False)

    
