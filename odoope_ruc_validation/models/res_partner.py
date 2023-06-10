from odoo import _, api, fields, models
import requests

DEFAULT_IAP_ENDPOINT = 'https://dniruc.apisperu.com/api/v1/'


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_country(self):
        return self.env.company.country_id.id

    country_id = fields.Many2one(default=_default_country)
    commercial_name = fields.Char(string="Commercial Name")
    state = fields.Selection([('habido', 'Habido'), ('nhabido', 'No Habido')], string="State")
    remote_id = fields.Char(string='Remote ID')
    alert_warning_vat = fields.Boolean(string="Alert warning vat", default=False)

    @api.model
    def l10n_pe_ruc_connection(self, vat_number):
        data = {}
        if self.env.company.l10n_pe_api_ruc_connection == 'consul_ruc_api':
            token = self.env.company.l10n_pe_partner_token
            data = self.fetch_ruc_data(vat_number, token)
        return data

    @api.model
    def l10n_pe_dni_connection(self, vat_number):
        data = {}
        if self.env.company.l10n_pe_api_dni_connection == 'consul_dni_api':
            token = self.env.company.l10n_pe_partner_token
            data = self.fetch_dni_data(vat_number, token)
        return data

    @api.onchange('vat', 'l10n_latam_identification_type_id')
    def onchange_vat(self):
        res = {}
        self.name = False
        self.commercial_name = False
        self.street = False
        self.city_id = False
        self.state_id = False
        self.l10n_pe_district = False
        if self.vat:
            if self.l10n_latam_identification_type_id.l10n_pe_vat_code == '6':
                if len(self.vat) != 11:
                    res['warning'] = {'title': _('Warning'), 'message': _('The RUC must be 11 characters long.')}
                else:
                    company = self.env['res.company'].browse(self.env.company.id)
                    if company.l10n_pe_ruc_validation:
                        self.get_data_ruc()
            elif self.l10n_latam_identification_type_id.l10n_pe_vat_code == '1':
                if len(self.vat) != 8:
                    res['warning'] = {'title': _('Warning'), 'message': _('The DNI must be 8 characters long.')}
                else:
                    company = self.env['res.company'].browse(self.env.company.id)
                    if company.l10n_pe_dni_validation:
                        self.get_data_dni()
        if res:
            return res

    def get_data_ruc(self):
        result = self.l10n_pe_ruc_connection(self.vat)
        if result:
            self.remote_id = result.get('ruc')
            self.alert_warning_vat = False
            self.company_type = 'company'
            self.name = result.get('razonSocial')
            self.commercial_name = result.get('nombreComercial') or result.get('razonSocial')
            self.street = result.get('direccion')
            self.state = 'habido' if result.get('condicion') == 'HABIDO' else 'nhabido'

            state_name = result.get('departamento')
            if state_name:
                state = self.env['res.country.state'].search(
                    [('name', '=ilike', state_name), ('country_id.code', '=', 'PE')], limit=1)
                if state:
                    self.state_id = state.id

            city_name = result.get('provincia')
            if city_name:
                city = self.env['res.city'].search([('name', '=ilike', city_name)], limit=1)
                if city:
                    self.city_id = city.id

                    district_name = result.get('distrito')
                    if district_name:
                        district = self.env['l10n_pe.res.city.district'].search([
                            ('name', '=ilike', district_name),
                            ('city_id', '=', city.id)
                        ], limit=1)
                        if district:
                            self.l10n_pe_district = district.id

    def get_data_dni(self):
        result = self.l10n_pe_dni_connection(self.vat)
        if result:
            self.remote_id = result.get('dni')
            self.alert_warning_vat = False
            self.company_type = 'person'
            self.name = f"{result.get('nombres')} {result.get('apellidoPaterno')} {result.get('apellidoMaterno')}"

    def fetch_ruc_data(self, vat_number, token):
        iap_server_url = DEFAULT_IAP_ENDPOINT
        endpoint = f"ruc/{vat_number}"
        params = {'token': token}
        url = f"{iap_server_url}{endpoint}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_dni_data(self, vat_number, token):
        iap_server_url = DEFAULT_IAP_ENDPOINT
        endpoint = f"dni/{vat_number}"
        params = {'token': token}
        url = f"{iap_server_url}{endpoint}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @api.onchange('l10n_pe_district')
    def _onchange_l10n_pe_district(self):
        if self.l10n_pe_district and self.l10n_pe_district.city_id:
            self.city_id = self.l10n_pe_district.city_id
            self.state_id = self.city_id.state_id.id

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id and self.city_id.state_id:
            self.state_id = self.city_id.state_id
        res = {}
        res['domain'] = {}
        res['domain']['l10n_pe_district'] = []
        if self.city_id:
            res['domain']['l10n_pe_district'] += [('city_id', '=', self.city_id.id)]
        return res

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id and self.state_id.country_id:
            self.country_id = self.state_id.country_id
        res = {}
        res['domain'] = {}
        res['domain']['city_id'] = []
        if self.state_id:
            res['domain']['city_id'] += [('state_id', '=', self.state_id.id)]
        return res













