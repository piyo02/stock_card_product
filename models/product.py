from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

class ProductStockCard(models.Model):
    _inherit = 'product.template'

    stock_card = fields.Float(
        'Quantity On Hand', compute='_compute_stock_card', search='_search_stock_card',
        digits=dp.get_precision('Product Unit of Measure'))

    def _compute_stock_card(self):
        return True

    def _search_stock_card(self):
        return True

    @api.multi
    def action_open_stock_card(self):
        stock_card = self.env['stock.card']
        
        products = self.mapped('product_variant_ids')
        stock_card.stock_card(products.ids[0])

        action = self.env.ref('stock_card_product.act_product_stock_card_open').read()[0]
        if products:
            action['context'] = {'default_product_id': products.ids[0]}
        action['domain'] = [('product_id.product_tmpl_id', 'in', self.ids)]
        return action