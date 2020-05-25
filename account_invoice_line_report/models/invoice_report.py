# -*- coding: utf-8 -*-
from . import library
import json
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InvoiceReport(models.Model):
    # _name= 'invoice.view'
    _inherit = 'account.invoice.report'


    def action_muki_connect(self):
        api = library.RestAPI()
        api.authenticate()
        # logging.info(str(api.execute('/api')))
        logging.info(str(api.execute('/api/user')))
