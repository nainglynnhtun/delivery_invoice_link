# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    invoice_ids = fields.Many2many(
        comodel_name="account.move",
        compute="_compute_invoice_ids",
        string="Invoices",
        readonly=True,
    )
    invoice_count = fields.Integer(
        string="Number of Invoices",
        compute="_compute_invoice_count",
    )

    @api.depends('sale_id', 'picking_type_id.code')
    def _compute_invoice_ids(self):
        for picking in self:
            if picking.sale_id and picking.picking_type_id.code == 'outgoing':
                # Only compute invoices for delivery orders
                picking.invoice_ids = picking.sale_id.invoice_ids
            else:
                picking.invoice_ids = self.env['account.move']

    def action_view_invoice(self):
        self.ensure_one()
        form_view_name = "account.view_move_form"
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_out_invoice_type"
        )
        if len(self.invoice_ids) > 1:
            result["domain"] = "[('id', 'in', %s)]" % self.invoice_ids.ids
        else:
            form_view = self.env.ref(form_view_name)
            result["views"] = [(form_view.id, "form")]
            result["res_id"] = self.invoice_ids.ids and self.invoice_ids.ids[0] or False
        return result

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)
