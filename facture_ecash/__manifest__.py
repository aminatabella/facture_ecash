# -*- coding: utf-8 -*-

{
    'name': 'Système de facturation E-CASH',
    'version': '1.0',
    'author': 'Bella Bah',
    'website': 'https://www.aminatabella.com',
    'support': 'baminatabella@gmail.com',
    'license': "AGPL-3",
    'complexity': 'easy',
    'sequence': 1,
    'category': 'Facturation',
    'description': """
        Système de facturation pour E-CASH en fonction de des besoins
    """,
    'depends': [
        'base',
        'account',
        'product',
        'mail'
    ],
    'summary': 'summary1, summary2, ',
    'data': [
        #'security/${ModuleName}.xml',
        #'security/ir.model.access.csv',
        #'data/${ModuleName}_data.xml',
        'views/facture_inherit.xml',
        'reports/report_invoice_inherit.xml',
        'menu.xml',
    ],
    'demo': [
    	#'demo/${ModuleName}_demo.xml'
    ],
    'css': [
    	#'static/src/css/${ModuleName}_style.css'
    ],

    'price': 0.00,
    'currency': 'EUR',
    'installable': True,
    'application': True,
}