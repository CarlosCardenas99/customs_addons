# -*- encoding: utf-8 -*-
import requests
import logging

from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

import requests
from io import StringIO
import io
import logging
from PIL import Image
from bs4 import BeautifulSoup
import time
import unicodedata
from . import servicio_busqueda

_logger = logging.getLogger(__name__)

class Partner(models.Model):
	_inherit = 'res.partner'

	# Para usar la funcion de busqueda desde llamadas javascript
	@api.model
	def consulta_datos_externos(self, tipo_documento, nro_documento, format='json'):
		datos = False
		datos_crear = {}
		if tipo_documento == "ruc":
			datos = servicio_busqueda.get_ruc_apisperu("", nro_documento)
			if not datos:
				return False
			datos_crear = {
				"name": datos['razonSocial'],
				"vat": nro_documento,
				"street": datos["direccion"],
				"zip": datos["ubigeo"],
				"l10n_latam_identification_type_id": self.env.ref('l10n_pe.it_RUC').id
			}
			ditrict_obj = self.env['l10n_pe.res.city.district']
			if datos.get('ubigeo'):
				ubigeo = datos.get('ubigeo')
				district = ditrict_obj.search([('code', '=', ubigeo)], limit=1)
			elif datos.get('distrito') and datos.get('provincia'):
				distrito = unicodedata.normalize('NFKD', datos.get('distrito')).encode('ASCII', 'ignore').strip().upper().decode()
				district = ditrict_obj.search([('name_simple', '=ilike', distrito), ('city_id', '!=', False)])
				if len(district) < 1:
					raise Warning('No se pudo ubicar el codigo de distrito'+distrito)
				elif len(district) > 1:
					district = ditrict_obj.search([('name_simple', '=ilike', distrito), ('city_id.name_simple', '=ilike', datos.get('provincia'))])
				if len(district) > 1:
					raise Warning('No se pudo establecer el codigo de distrito, mas de una opcion encontrada')
				elif len(district) < 1:
					raise Warning('No se pudo ubicar el codigo de distrito, se perdio en la validacion '+distrito+' '+datos.get('provincia')+' '+datos.get('departamento')) 

			if district:
				datos_crear["l10n_pe_district"] = district.id
				datos_crear["city_id"] = district.city_id.id
				datos_crear["state_id"] = district.city_id.state_id.id
				datos_crear["country_id"] = district.city_id.state_id.country_id.id

		elif tipo_documento == "dni":
			datos = servicio_busqueda.get_dni_apisperu("", nro_documento)
			if not datos:
				return False
			if 'error' in datos and datos['error'] == True:
				return False

			nombre = "%s, %s %s" % (datos['nombres'], datos['apellidoPaterno'], datos['apellidoMaterno'])
			datos_crear = {
				"name": nombre,
				"vat": nro_documento,
				"l10n_latam_identification_type_id": self.env.ref('l10n_pe.it_DNI').id
			}


		if datos:
			contacto = self.env['res.partner'].create(datos_crear)
			if contacto:
				return contacto.id
		
		return False