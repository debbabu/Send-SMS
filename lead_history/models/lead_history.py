import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

class field_history(models.Model):
    _name = "field_history"
    _description = "Field Details"

    create_date = fields.Datetime('Update Date', readonly=True)
    lead_name = fields.Many2one('lead_history', string="Lead Name")
    field_name = fields.Char(string="Field Name")
    field_value = fields.Char(string="Field Value")

    def create_field_history(self, lead_history_ids, vals):
        value = {}
        for lead_history_id in lead_history_ids:
            for val in vals:
                value['lead_name'] = lead_history_id
                field_id = self.env["ir.model.fields"].search([('name','=',val),('model','=','crm.lead')])
                value['field_name'] = field_id.field_description
                if field_id.ttype == 'one2many' or field_id.name == 'date_action_last':
                    continue
                elif field_id.ttype == 'many2one':
                    rel_data = (self.env[field_id.relation].browse(vals[val])).display_name
                    value['field_value'] = rel_data
                elif field_id.ttype == 'many2many':
                    m2m_datas = []
                    rel_ids = (vals[val])[0][(len((vals[val])[0]))-1]
                    for rel_id in rel_ids:
                        rel_data = (self.env[field_id.relation].browse(rel_id,)).display_name
                        m2m_datas.append(rel_data)
                    value['field_value'] = m2m_datas
                else:
                    value['field_value'] = vals[val]
                self.create(value)

class lead_history(models.Model):
    _name = "lead_history"
    _description = "Lead History"

    name = fields.Many2one('crm.lead', string="Lead Name")
    original_name = fields.Char(string="Original Name")
    email = fields.Char(string="Eamil")
    mobile = fields.Char(string="Mobile")
    field_history_id = fields.One2many('field_history','lead_name',string="Field Details")

    def create_lead_history(self, ids, vals):
        val={}
        lead_history_id = []

        if isinstance(ids, list):
            for lid in ids:
                lid_id = self.search([('name','=',lid)])
                if not lid_id:
                    val['name'] = lid
                    lead_data = self.env["crm.lead"].search_read([('id','=',lid)])
                    if 'name' in lead_data[0]:
                        val['original_name'] = lead_data[0]['name']
                    if 'email_from' in lead_data[0]:
                        val['email'] = lead_data[0]['email_from']
                    if 'x_email' in lead_data[0] and not val['email']:
                        val['email'] = lead_data[0]['x_email']
                    if 'mobile' in lead_data[0]:
                        val['mobile'] = lead_data[0]['mobile']
                    lid_id = self.create(val)
                    lead_history_id.append(lid_id.id)
                else:
                    if 'email_from' in vals:
                        val['email'] = vals['email_from']
                    if 'x_email' in vals and 'email' not in val:
                          val['email'] = vals['x_email']
                    if 'mobile' in vals:
                        val['mobile'] = vals['mobile']
                    if val:
                        lid_id.write(val)
                    lead_history_id.append(lid_id.id)
        return lead_history_id

class Lead(models.Model):
    _inherit = "crm.lead"

    @api.multi
    def write(self, vals):
        lead_status = super(Lead, self).write(vals)
        lead_history_ids = self.env["lead_history"].create_lead_history(self.ids, vals)
        if lead_history_ids:
            self.env["field_history"].create_field_history(lead_history_ids, vals)
        return lead_status
