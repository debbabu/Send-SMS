import logging
from openerp.osv import fields,osv,expression
from openerp import models,api
_logger = logging.getLogger(__name__)

class field_details(osv.osv):
    _name = "field_details"
    _description = "Field Details"

    _columns={
        'create_date': fields.datetime('Update Date', readonly=True),
        'lead_name': fields.many2one('lead_details', string="Lead Name"),
        'field_name': fields.char(string="Field Name"),
        'field_value': fields.char(string="Field Value"),
    }

    def create_field_details(self, cr, uid, lead_detail_ids, vals):
        value = {}
        for lead_detail_id in lead_detail_ids:
            for val in vals:
                value['lead_name'] = lead_detail_id
                # _logger.info(val)
                field_id = self.pool.get("ir.model.fields").search(cr, uid,[('name','=',val),('model','=','crm.lead')])
                field_data = self.pool.get("ir.model.fields").browse(cr, uid, field_id, [])
                # _logger.info(field_data)
                value['field_name'] = field_data.field_description
                if field_data.ttype == 'one2many' or field_data.name == 'date_action_last':
                    continue
                elif field_data.ttype == 'many2one':
                    rel_data = (self.pool.get(field_data.relation).browse(cr, uid, vals[val], [])).display_name
                    value['field_value'] = rel_data
                elif field_data.ttype == 'many2many':
                    m2m_datas = []
                    rel_ids = (vals[val])[0][(len((vals[val])[0]))-1]
                    for rel_id in rel_ids:
                        rel_data = (self.pool.get(field_data.relation).browse(cr, uid, rel_id, [])).display_name
                        m2m_datas.append(rel_data)
                    value['field_value'] = m2m_datas
                else:
                    value['field_value'] = vals[val]
                self.create(cr, uid, value)

class lead_details(osv.osv):
    _name = "lead_details"
    _description = "Lead Details"

    _columns={
        'name': fields.many2one('crm.lead', string="Lead Name"),
        'original_name': fields.char(string="Original Name"),
        'email': fields.char(string="Eamil"),
        'mobile': fields.char(string="Mobile"),
        'field_detail_id': fields.one2many('field_details','lead_name',string="Field Details"),
    }
    def create_lead_details(self, cr, uid, ids, vals):
        val={}
        lead_detail_id = []
        if isinstance(ids, list):
            for lid in ids:
                lid_id = self.search(cr, uid,[('name','=',lid)])
                if not lid_id:
                    val['name'] = lid
                    lead_detail = self.pool.get("crm.lead").read(cr, uid,lid,[])
                    if 'name' in lead_detail:
                        val['original_name'] = lead_detail['name']
                    if 'email_from' in lead_detail:
                        val['email'] = lead_detail['email_from']
                    if 'x_email' in lead_detail and not val['email']:
                        val['email'] = lead_detail['x_email']
                    if 'mobile' in lead_detail:
                        val['mobile'] = lead_detail['mobile']
                    lid_id = self.create(cr, uid, val)
                    lead_detail_id.append(lid_id)
                else:
                    lid_id_detail = self.read(cr, uid,lid_id,[])
                    if 'email_from' in vals:
                        val['email'] = vals['email_from']
                    if 'x_email' in vals and 'email' not in val:
                          val['email'] = vals['x_email']
                    if 'mobile' in vals:
                        val['mobile'] = vals['mobile']
                    if val:
                        self.write(cr,uid,lid_id[0],val)
                    lead_detail_id.append(lid_id[0])
        return lead_detail_id
    @api.multi
    def print_lead(self):
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'lead_details.lead_report')
class crm_lead(osv.osv):
    _inherit = "crm.lead"

    def write(self, cr, uid, ids, vals, context=None):
        lead_status = super(crm_lead, self).write(cr, uid, ids, vals, context=context)
        lead_detail_ids = self.pool.get("lead_details").create_lead_details(cr, uid, ids, vals)
        if lead_detail_ids:
            self.pool.get("field_details").create_field_details(cr, uid, lead_detail_ids, vals)
        return lead_status
