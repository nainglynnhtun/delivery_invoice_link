# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Invoice Link With Delivery Orders",
    'description': """
    - Customer Invoice Link With Only Delivery Orders
    - Delivery Orders Link with Customer Invoice
    """,
    "version": "16.0",
    "category": "Warehouse Management",
    "summary": "Adds link between pickings and invoices",
    'author': 'Naing Lynn Htun',
    'support': 'konainglynnhtun@gmail.com',
    'license': 'LGPL-3',
    "depends": ["sale_stock","sale"],
    "data": [
        "views/account_invoice_view.xml",
        "views/stock_view.xml"
    ],
    'images': ['static/description/banner.png'],
    "installable": True,
    'auto_install': False,
}
