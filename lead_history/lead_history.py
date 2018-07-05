import logging
from openerp.osv import fields,osv,expression
from openerp import models,api
_logger = logging.getLogger(__name__)

class field_history(osv.osv):
    _name = "field_history"
    _description = "Field Details"

    _columns={
        'create_date': fields.datetime('Update Date', readonly=True),
        'lead_name': fields.many2one('lead_history', string="Lead Name"),
        'field_name': fields.char(string="Field Name"),
        'field_value': fields.char(string="Field Value"),
    }

    def create_field_history(self, cr, uid, lead_history_ids, vals):
        value = {}
        for lead_history_id in lead_history_ids:
            for val in vals:
                value['lead_name'] = lead_history_id
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

class lead_history(osv.osv):
    _name = "lead_history"
    _description = "Lead Details"

    _columns={
        'name': fields.many2one('crm.lead', string="Lead Name"),
        'original_name': fields.char(string="Original Name"),
        'email': fields.char(string="Eamil"),
        'mobile': fields.char(string="Mobile"),
        'field_history_id': fields.one2many('field_history','lead_name',string="Field Details"),
    }
    def create_lead_history(self, cr, uid, ids, vals):
        val={}
        lead_history_id = []
        if isinstance(ids, list):
            for lid in ids:
                lid_id = self.search(cr, uid,[('name','=',lid)])
                if not lid_id:
                    val['name'] = lid
                    lead_data = self.pool.get("crm.lead").read(cr, uid,lid,[])
                    if 'name' in lead_data:
                        val['original_name'] = lead_data['name']
                    if 'email_from' in lead_data:
                        val['email'] = lead_data['email_from']
                    if 'x_email' in lead_data and not val['email']:
                        val['email'] = lead_data['x_email']
                    if 'mobile' in lead_data:
                        val['mobile'] = lead_data['mobile']
                    lid_id = self.create(cr, uid, val)
                    lead_history_id.append(lid_id)
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
                    lead_history_id.append(lid_id[0])
        return lead_history_id
    @api.multi
    def print_lead(self):
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'lead_history.lead_report')
class crm_lead(osv.osv):
    _inherit = "crm.lead"

    def write(self, cr, uid, ids, vals, context=None):
        lead_status = super(crm_lead, self).write(cr, uid, ids, vals, context=context)
        lead_history_ids = self.pool.get("lead_history").create_lead_history(cr, uid, ids, vals)
        if lead_history_ids:
            self.pool.get("field_history").create_field_history(cr, uid, lead_history_ids, vals)
        return lead_status
