from odoo import models, fields, api

class SalesOrderInherit(models.Model):

    _inherit = 'sale.order'

    ref_nos = fields.Many2one('res.partner',string='Reference No:')