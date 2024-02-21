# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        string="Related Pickings",
        store=True,
        compute="_compute_picking_ids",
        help="Related pickings (only when the invoice has been generated from a sale order).",
    )

    delivery_count = fields.Integer(
        string="Delivery Orders", compute="_compute_picking_ids", store=True
    )
    
    @api.depends('line_ids.sale_line_ids')
    def _compute_picking_ids(self):
        for invoice in self:
            # Initialize an empty set to hold unique picking ids
            pickings = set()
            # Iterate over each invoice line
            for line in invoice.invoice_line_ids:
                # For each sale line related to the invoice line
                for sale_line in line.sale_line_ids:
                    # Access the order of the sale line and then its pickings
                    order_pickings = sale_line.order_id.picking_ids
                    # Filter for pickings with type 'outgoing' (deliveries)
                    delivery_pickings = order_pickings.filtered(lambda p: p.picking_type_id.code == 'outgoing')
                    # Add the picking ids to the set
                    pickings.update(delivery_pickings.ids)
            
            # Convert the set of picking ids to recordset
            invoice.picking_ids = self.env['stock.picking'].browse(list(pickings))
            invoice.delivery_count = len(invoice.picking_ids)

    # @api.depends("invoice_line_ids")
    # def _compute_picking_ids(self):
    #     for invoice in self:
    #         # Initialize an empty set to hold unique picking ids
    #         pickings = set()
    #         # Iterate over each invoice line
    #         for line in invoice.invoice_line_ids:
    #             # For each sale line related to the invoice line
    #             for sale_line in line.sale_line_ids:
    #                 # Access the order of the sale line and then its pickings
    #                 order_pickings = sale_line.order_id.picking_ids
    #                 # Add the picking ids to the set
    #                 pickings.update(order_pickings.ids)
            
    #         # Convert the set of picking ids to recordset
    #         invoice.picking_ids = self.env['stock.picking'].browse(list(pickings))
    #         invoice.delivery_count = len(invoice.picking_ids)

    def action_show_picking(self):
        """This function returns an action that display existing pickings
        of given invoice.
        It can either be a in a list or in a form view, if there is only
        one picking to show.
        """
        self.ensure_one()
        form_view_name = "stock.view_picking_form"
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "stock.action_picking_tree_all"
        )
        if len(self.picking_ids) > 1:
            result["domain"] = "[('id', 'in', %s)]" % self.picking_ids.ids
        else:
            form_view = self.env.ref(form_view_name)
            result["views"] = [(form_view.id, "form")]
            result["res_id"] = self.picking_ids.id
        return result
