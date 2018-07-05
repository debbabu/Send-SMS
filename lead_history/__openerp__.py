# -*- coding: utf-8 -*-
{
    'name': "Lead History",
    'summary': """It fetch the history of a lead""",
    'description': """

=======================

This module show the history of the lead. When any lead update it shows, which field updated.
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
    'installable':True,
    'auto_install':False,
}
