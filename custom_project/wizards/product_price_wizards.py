from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductPrice(models.TransientModel):

    _name = 'product.price.wizards'

    def _default_prod(self):
        return self.env['project.product'].browse(self._context.get('active_ids'))

    proj_id = fields.Many2one('project.site',string='Project:')
    apartment_id = fields.Many2one('project.product',string='Apartment:')


    building_no = fields.Char(string='Building No:')
    floor_no = fields.Char(string='Floor No:')
    type_id = fields.Char(string='Apartment Type:')
    prod_price = fields.Float(string="Unit Price:")
    ext_unit_price = fields.Integer(string='Exterior Unit Price:')
    inter_unit_price = fields.Integer(string='Interior Unit Price:')
    unit_price = fields.Selection([('single','Unit Price'),('multiple','Multiple Unit Price')],string='Apartment Price:')

    @api.onchange('proj_id')
    def apartment_domain(self):
        for rec in self:
            return {'domain': {'apartment_id': [('project_no.id', '=', rec.proj_id.id)]}}

    @api.onchange('proj_id','apartment_id')
    def update_apartment_details(self):
        for rec in self:
            if rec.apartment_id:
                rec.building_no = rec.apartment_id.building_no
                rec.floor_no = rec.apartment_id.floor_no
                rec.type_id = rec.apartment_id.type_id
                rec.prod_price = rec.apartment_id.proj_price
                rec.ext_unit_price = rec.apartment_id.ext_price
                rec.inter_unit_price = rec.apartment_id.interior_price


    def price_update(self):

        filter_list = []

        if self.proj_id:
            filter_list.append(('project_no', '=', self.proj_id.id))
        else:
            raise ValidationError(('Oops!!! Select the Project First!!'))
        if self.building_no:
            filter_list.append(('building_no', '=', self.building_no))
        if self.floor_no:
            filter_list.append(('floor_no', '=', self.floor_no))
        if self.type_id:
            filter_list.append(('type_id', '=', self.type_id))
        prod_obj = self.env['project.product'].search(filter_list)
        print('hello')
        for record in prod_obj:
            record.proj_price = self.prod_price
            record.total_price = (record.carpet_area_no + record.terrace_area_no) * record.proj_price
        for record in prod_obj:
            record.interior_price = self.inter_unit_price
            record.ext_price = self.ext_unit_price
            record.total_price = record.carpet_area_no * record.interior_price + record.terrace_area_no * record.ext_price


    def cancel(self):
        """To close wizard"""
        return {'type': 'ir.actions.act_window_close'}