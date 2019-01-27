# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class HttpIntegrateController(http.Controller):
    @http.route('/post-api',type='http', auth='none', methods=['POST'], csrf=False)
    def post_api(self, **kwargs):
        if 'user' in kwargs and 'password' in kwargs:
            record_status = request.env['http_api'].sudo().create_record(kwargs)
            if record_status:
                return record_status
            return '{Status: Fail, Error: user or password may be wrong}'
        return '{Status: Fail, Error: Add user or password}'

    @http.route('/get-api',type='http', auth='none', methods=['GET'], csrf=False)
    def get_api(self, **kwargs):
        if 'user' in kwargs and 'password' in kwargs:
            record_status = request.env['http_api'].sudo().create_record(kwargs)
            if record_status:
                return record_status
            return '{Status: Fail, Error: user or password may be wrong}'
        return '{Status: Fail, Error: Add user or password}'
