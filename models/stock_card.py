from odoo import api, fields, models, _
    
class StockCard(models.Model):
    _name = "stock.card"
    
    date			= fields.Date("Date")
    location_id		= fields.Many2one('stock.location', 'Location', required=True)
    product_id		= fields.Many2one('product.product', 'Product', required=True)
    picking_id		= fields.Many2one('stock.picking', 'Picking')
    qty_start		= fields.Float("Start")
    qty_in			= fields.Float("Qty In")
    qty_out			= fields.Float("Qty Out")
    qty_balance		= fields.Float("Balance")
    product_uom_id	= fields.Many2one('product.uom', 'UoM')
    description		= fields.Char("Description")

    @api.multi
    def action_open_stock_card(self):
        products = self.mapped('product_variant_ids')
        action = self.env.ref('stock.product_open_quants').read()[0]
        action['domain'] = [('product_id', 'in', products.ids)]
        action['context'] = {'search_default_locationgroup': 1, 'search_default_internal_loc': 1}
        return action