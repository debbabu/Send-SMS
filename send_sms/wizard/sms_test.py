from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.exceptions import except_orm, UserError

import logging
_logger = logging.getLogger(__name__)

class SMSTest(models.TransientModel):
    _name = 'sms.test'
    _description = 'SMS Test wizard'
    _log_access = True

    test_result = fields.Text('Message')
    # mobile = fields.Char('Mobile')

    # @api.one
    # def sms_test_action(self):
    #     active_id = self.env.context.get('active_id')
    #     active_model = self._context['active_model']
    #     getway_id = self.env[active_model].search([('id','=',active_id)])
    #     message = self.env['send_sms'].render_template(self.message, active_model, active_id)
    #     mobile_no = self.env['send_sms'].render_template(self.mobile, active_model, active_id)
    #     response = self.env['send_sms'].send_sms_link(message, mobile_no,active_id,active_model,getway_id)
    #     if response:
    #         raise UserError(_(response))
    #     return True
