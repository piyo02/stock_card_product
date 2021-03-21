from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = "stock.move"
    _name = "stock.move"

    has_count = fields.Boolean(string="Telah di Hitung", readonly=True, default=False)