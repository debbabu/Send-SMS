# -*- coding: utf-8 -*-
{
    'name': "HTTP API",
    'summary': """You can create record using GET or POST method of RESTfull API.""",
    'author': "Debasish",
    'website': "http://www.debweb.com",
    'category': 'API',
    'version': '12.0.1',
    'depends': ['base','web',],
    'data': [
        'view/http_api_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        ],
    'images':['static/description/banner-1.png'],
    'license': 'LGPL-3',
    'installable':True,
    'auto_install':False,
}
