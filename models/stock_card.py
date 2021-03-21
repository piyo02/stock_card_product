from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class StockCard(models.Model):
    _name = "stock.card"
    
    date			= fields.Datetime("Tanggal")
    description		= fields.Char("Deskripsi")
    information		= fields.Char("Deskripsi")
    loc_id          = fields.Many2one('stock.location', 'Lokasi', required=True)
    location_id		= fields.Many2one('stock.location', 'Lokasi Sumber', required=True)
    location_dest_id= fields.Many2one('stock.location', 'Lokasi Tujuan', required=True)
    picking_id		= fields.Many2one('stock.picking', 'Picking')
    product_id		= fields.Many2one('product.product', 'Produk', required=True)
    qty_start		= fields.Float("Qty Awal")
    qty_in			= fields.Float("Qty Masuk")
    qty_out			= fields.Float("Qty Keluar")
    qty_balance		= fields.Float("Qty Akhir")

    @api.model
    def stock_card(self, product_id):
        # mengambil seluruh stock move untuk product
        moves = self.env['stock.move'].search([
            ("product_id.id", "=", product_id),
            ("has_count", "=", False),
            ("state", "=", "done"),
        ], order="date asc")

        # membuat array untuk warehouse internal location 
        warehouses = []
        warehouse_int = self.env['stock.location'].search([
            ('usage', '=', 'internal')
        ])
        for warehouse in warehouse_int:
            warehouses.append(warehouse.location_id.name)

        for move in moves:
            stock_cards = self.env['stock.card'].search([
                ('date', '<=', move.date),
                ("product_id.id", "=", product_id),
            ], order="date desc, id desc")

            move.write({ 'has_count': True })
            information = ""
            if move.location_id.location_id.name in warehouses:
                loc_id = move.location_id.id
                description = "Barang Keluar dari " + move.location_id.location_id.name
                qty_start = 0
                for stock_card in stock_cards:
                    if move.location_id.location_id.name in stock_card.description:
                        qty_start = stock_card.qty_balance
                        break

                if move.picking_id.name:
                    if "/IN/" in move.picking_id.name:
                        information = "Pembelian"
                    if "POS" in move.picking_id.name:
                        information = "Penjualan Kasir"
                    if "/OUT/" in move.picking_id.name:
                        information = "Penjualan"
                    if "/INT/" in move.picking_id.name:
                        information = "Transfer Item dari " + move.location_id.location_id.name + " ke " + move.location_dest_id.location_id.name
                    if "RP" in move.picking_id.name:
                        information = "Produksi"
                
                qty_out = move.product_uom_qty
                qty_in = 0
                qty_balance = qty_start + (qty_in -  qty_out)
                self.create_stock_card({ 
                    'product_id': move.product_id.id, 'date': move.date, 'information': information, 'description': description, 'loc_id': loc_id,
                    'location_id': move.location_id.id, 'location_dest_id': move.location_dest_id.id,'picking_id': move.picking_id.id,
                    'qty_start': qty_start,'qty_in': qty_in,'qty_out': qty_out,'qty_balance': qty_balance
                })

            if move.location_dest_id.location_id.name in warehouses:
                loc_id = move.location_dest_id.id
                description = "Barang Masuk ke " + move.location_dest_id.location_id.name
                qty_start = 0
                for stock_card in stock_cards:
                    if move.location_dest_id.location_id.name in stock_card.description:
                        qty_start = stock_card.qty_balance
                        break
                
                if move.picking_id.name:
                    if "/IN/" in move.picking_id.name:
                        information = "Pembelian"
                    if "POS" in move.picking_id.name:
                        information = "Penjualan Kasir"
                    if "WH/OUT" in move.picking_id.name:
                        information = "Penjualan"
                    if "/INT/" in move.picking_id.name:
                        information = "Transfer Item dari " + move.location_id.location_id.name + " ke " + move.location_dest_id.location_id.name
                    if "RP" in move.picking_id.name:
                        information = "Produksi"
                    if move.picking_id.name == False:
                        information = "Saldo Awal"
                
                qty_in = move.product_uom_qty
                qty_out = 0
                qty_balance = qty_start + (qty_in -  qty_out)
                self.create_stock_card({ 
                    'product_id': move.product_id.id, 'date': move.date, 'information': information, 'description': description, 'loc_id': loc_id,
                    'location_id': move.location_id.id, 'location_dest_id': move.location_dest_id.id,'picking_id': move.picking_id.id,
                    'qty_start': qty_start,'qty_in': qty_in,'qty_out': qty_out,'qty_balance': qty_balance
                })

    @api.model
    def create_stock_card( self, vals ):
        res = super(StockCard, self).create(vals)
        return res