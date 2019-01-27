import logging
from odoo import api, fields, models, tools, SUPERUSER_ID
import json, ast

_logger = logging.getLogger(__name__)

class HttpAPI(models.Model):
    _name = "http_api"
    _description = "HTTP API"

    model_id = fields.Many2one('ir.model',string="Model")
    user = fields.Char('User')
    password = fields.Char('Password')

    @api.model
    def create_record(self, data_dict):
        body_data = data_dict.copy()
        http_user = self.search([('user','=',data_dict['user'])],limit=1)
        if http_user and http_user.password == data_dict['password']:
            for field_name in data_dict:
                field_id = self.env["ir.model.fields"].sudo().search([('name','=',field_name),('model_id','=',http_user.model_id.id)])
                if field_id.ttype == 'many2one':
                    if field_id.name in data_dict:
                        data_dict[field_id.name] = data_dict[field_id.name].upper().strip()
                        if 'x_' in field_id.relation:
                            field_cr = self.env[field_id.relation].sudo().search([('x_name', '=ilike', data_dict[field_id.name])], limit=1)
                        else:
                            field_cr = self.env[field_id.relation].sudo().search([('name', '=ilike', data_dict[field_id.name])], limit=1)
                        if len(field_cr) == 0 and data_dict[field_id.name].encode('ascii', 'ignore').isdigit():
                            field_cr = self.env[field_id.relation].sudo().search([('id', '=', data_dict[field_id.name])], limit=1)
                        if len(field_cr) > 0:
                            data_dict[field_id.name] = field_cr[0].id
                        else:
                            data_dict[field_id.name] = ''
                if field_id.ttype == 'many2many':
                    if field_id.name in data_dict:
                        many2many_list = []
                        many2many_datas = data_dict[field_id.name].split(',')
                        for many2many_data in many2many_datas:
                            many2many_data = many2many_data.strip()
                            if 'x_' in field_id.relation:
                                field_cr = self.env[field_id.relation].sudo().search([('x_name', '=ilike', many2many_data)], limit=1)
                            else:
                                field_cr = self.env[field_id.relation].sudo().search([('name', '=ilike', many2many_data)], limit=1)
                            if len(field_cr) == 0 and data_dict[field_id.name].encode('ascii', 'ignore').isdigit():
                                field_cr = self.env[field_id.relation].sudo().search([('id', '=', many2many_data)], limit=1)

                            if len(field_cr) > 0:
                                many2many_list.append(field_cr.id)

                        if many2many_list:
                            data_dict[field_id.name] = [(6, 0,many2many_list)]

                if field_id.ttype == 'selection':
                    if field_id.name in data_dict:
                        c=0
                        board_list=dict(self.env[http_user.model_id.name].fields_get(allfields=[field_id.name]))[field_id.name]['selection']
                        for board_items in board_list:
                            if (board_items[1].upper()== data_dict[field_id.name].strip().upper()):
                                data_dict[field_id.name]=board_items[0]
                                c=c+1
                        if(c==0):
                            data_dict[field_id.name] = ''
            if 'source_id' not in data_dict:
                source_cr = self.env["utm.source"].sudo().search([('name', '=ilike', data_dict['user'])], limit=1)
                if len(source_cr) > 0:
                    data_dict['source_id'] = source_cr[0].id

            data_dict.pop('user', None)
            data_dict.pop('password', None)
            data_dicts = {}
            for data in data_dict:
                if data_dict[data] != '':
                    data_dicts[data] = data_dict[data]

            if data_dicts:
                record_id = self.env[http_user.model_id.model].sudo().create(data_dicts)
                if record_id:
                    body_data.pop('password', None)
                    message_id = self.env['mail.message'].sudo().create({'body':ast.literal_eval(json.dumps(body_data)),'model':http_user.model_id.model,'message_type':'email','res_id':record_id.id})
                    return '{Status: Success, Lead Id: '+str(record_id.id)+'}'
                else:
                    return '{Status: Fail, Error: Please contact system admin}'
            else:
                return '{Status: Fail, Error: Data not available}'
        return
