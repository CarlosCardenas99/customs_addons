# -*- encoding: utf-8 -*-
import requests
import logging

from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from io import StringIO
import io
import logging
from PIL import Image
from bs4 import BeautifulSoup
import time
import unicodedata
import os

_logger = logging.getLogger(__name__)


# ::::::::::::::::: Usando API de apisperu
def get_dni_apisperu(token, dni):
	token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNyZWF0aXZlLnN0b3JlLnBhbHRhcnVtaUBnbWFpbC5jb20ifQ.ocVpoFaQU-1sNAkEWVEGTmaZm4UcFsRXwigiY4zFkm0'
	endpoint = "https://dniruc.apisperu.com/api/v1/dni/%s?%s" % (dni, token)
	headers = {
		"Authorization": "Bearer %s" % token,
		"Content-Type": "application/json",
	}
	try:
		datos_dni = requests.get(endpoint, data={}, headers=headers)
		if datos_dni.status_code == 200:
			datos = datos_dni.json()
			return datos
		else:
			return False
	except Exception as e:
		return False

def get_ruc_apisperu(token, ruc):
	try:
		token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNyZWF0aXZlLnN0b3JlLnBhbHRhcnVtaUBnbWFpbC5jb20ifQ.ocVpoFaQU-1sNAkEWVEGTmaZm4UcFsRXwigiY4zFkm0'
		endpoint = "https://dniruc.apisperu.com/api/v1/ruc/%s?%s" % (ruc, token)
		headers = {
			"Authorization": "Bearer %s" % token,
			"Content-Type": "application/json",
		}
		datos_ruc = requests.get(endpoint, data={}, headers=headers)
		if datos_ruc.status_code == 200:
			datos_ruc = datos_ruc.json()
			return datos_ruc
		else:
			return False
	except Exception as e:
		return False
