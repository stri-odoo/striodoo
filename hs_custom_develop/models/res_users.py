# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

import requests

from odoo import api, fields, models
from odoo.exceptions import AccessDenied, UserError

import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
	_inherit = 'res.users'


	@api.model	
	def _auth_oauth_rpc(self, endpoint, access_token):
		# _logger.info("El valor de _auth_oauth_rpc es:")
		# _logger.info("endpoint: {} - token: {}".format(str(endpoint), str(access_token)))
		try:
			super(ResUsers, self)._auth_oauth_rpc(endpoint, access_token)
		except Exception as __ERROR:
			# respuesta = requests.get(endpoint, params={'access_token': access_token})
			# _logger.info("El valor de respuesta es {}".format(respuesta.text))
			# return respuesta.json()
			HEADERS = {
				'Authorization': 'Bearer ' + access_token,
				'Accept':  'application/json',
			}
			resp = requests.get(endpoint, headers=HEADERS).json()
			user_id = self.env['res.users'].sudo().search([('login', '=', resp.get('email'))], limit=1)
			if user_id:
				if user_id.oauth_uid == False or user_id.oauth_uid == "":
					oauth_uid = str(resp.get('user_id'))
					user_id.write({'oauth_uid':oauth_uid})
			return resp
