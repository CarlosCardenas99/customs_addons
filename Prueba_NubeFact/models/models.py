import json
import requests
from datetime import date, timedelta
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    sunat_response = fields.Text(string='Respuesta de SUNAT')

    envios_sunat = fields.Boolean(string='Envíos a SUNAT', compute='_compute_envios_sunat')

    def _compute_envios_sunat(self):
        for record in self:
            record.envios_sunat = bool(record.sunat_response)

    def send_to_sunat(self):
        for record in self:
            # Ruta y Token para trabajar con NubeFact
            ruta = "https://api.nubefact.com/api/v1/50242799-d1b4-4a90-b696-5d659b3c6f07"
            token = "bd8fbab252994dda974a089555979682cbca855e82ac42059fad8ec9b9023a23"

            # Obtener los datos necesarios del registro actual
            partner = record.partner_id
            if not partner.vat or not partner.vat.strip():
                raise ValueError("El cliente no tiene un número de documento válido.")

            # Obtener los valores de los items de la factura de Odoo
            items = []
            total_igv = 0.0  # Variable para sumar los montos del IGV en las líneas
            for line in record.invoice_line_ids:
                # Calcular el monto del IGV en la línea
                igv = line.price_subtotal * (line.tax_ids.amount / 100)
                total_igv += igv  # Sumar el monto del IGV a la variable total_igv

                item = {
                    "unidad_de_medida": "NIU",
                    "codigo": line.product_id.default_code,
                    "descripcion": line.name,
                    "cantidad": str(line.quantity),
                    "valor_unitario": str(line.price_unit),
                    "precio_unitario": str(line.price_unit * (1 + line.tax_ids.amount / 100)),
                    "descuento": "",
                    "subtotal": str(line.price_subtotal),
                    "tipo_de_igv": "1",
                    "igv": str(igv),  # Utilizar el monto del IGV calculado
                    "total": str(line.price_total),
                    "anticipo_regularizacion": "false",
                    "anticipo_documento_serie": "",
                    "anticipo_documento_numero": ""
                }
                items.append(item)

            invoice = {
                "operacion": "generar_comprobante",
                "tipo_de_comprobante": "1",
                "serie": "FFF1",
                "numero": "15",
                "sunat_transaction": "1",
                "cliente_tipo_de_documento": "6",
                "cliente_numero_de_documento": partner.vat,
                "cliente_denominacion": partner.name,
                "cliente_direccion": partner.street,
                "cliente_email": partner.email,
                "cliente_email_1": "",
                "cliente_email_2": "",
                "fecha_de_emision": fields.Date.context_today(self).strftime('%Y-%m-%d'),
                "fecha_de_vencimiento": str(fields.Date.today() + timedelta(days=3)),
                "moneda": "1",
                "tipo_de_cambio": "",
                "porcentaje_de_igv": 18.00,
                "descuento_global": "",
                "total_descuento": "",
                "total_anticipo": "",
                "total_gravada": record.amount_untaxed,
                "total_inafecta": "",
                "total_exonerada": "",
                "total_igv": str(total_igv),  # Utilizar el total del IGV calculado
                "total_gratuita": "",
                "total_otros_cargos": "",
                "total": str(record.amount_total),
                "percepcion_tipo": "",
                "percepcion_base_imponible": "",
                "total_percepcion": "",
                "detraccion": False,
                "accion": False,
                "observaciones": "",
                "documento_que_se_modifica_tipo": "",
                "documento_que_se_modifica_serie": "",
                "documento_que_se_modifica_numero": "",
                "items": items
            }

            # Convertir el diccionario a formato JSON
            json_data = json.dumps(invoice)

            # Configurar los encabezados de la solicitud
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Token token=\"{token}\""
            }

            try:
                # Enviar la solicitud a NubeFact con verificación del certificado SSL
                response = requests.post(
                    ruta,
                    data=json_data,
                    headers=headers,
                    verify=True
                )

                # Procesar la respuesta recibida
                if response.status_code == 200:
                    result = response.json()
                    if result.get("errors"):
                        error_message = result["errors"][0]["message"]
                        raise ValueError(f"Error al generar el comprobante: {error_message}")
                    else:
                        numero_comprobante = result["numero_comprobante"]
                        url_pdf = result["enlace_del_pdf"]
                        url_xml = result["enlace_del_xml"]
                        record.sunat_response = f"Comprobante generado: {numero_comprobante}\nPDF: {url_pdf}\nXML: {url_xml}"
                else:
                    raise ValueError(f"Error en la solicitud. Código de respuesta: {response.status_code}")
            except requests.exceptions.RequestException as e:
                raise ValueError(f"Error en la solicitud: {str(e)}")





