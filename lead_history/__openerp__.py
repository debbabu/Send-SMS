# -*- coding: utf-8 -*-
{
    'name': "Lead History",
    'summary': """It fetch the history of a lead""",
    'description': """

=======================

1. This module show the history of the lead. When any lead update it shows, which field updated with field value.
2. You can print all that history of lead as a report.
3. You can find Lead History menu under Report Section of Sales menu.

   Sales > Reports > Lead History
    """,
    'author': "Debasisa Dash",
    'website': "http://www.fdshive.com",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base','web','crm'],
    'data': [
        'view/lead_history_view.xml',
        'view/lead_history_report.xml',
        'view/report_lead.xml',
        'security/ir.model.access.csv',
    ],

    'demo': [
        ],
    'images':['static/description/banner.png'],
    'installable':True,
    'auto_install':False,
}
