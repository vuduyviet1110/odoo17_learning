from odoo import fields, models, api

class EducationSchool(models.Model):
    _name = 'education.school'
    _description = 'School'

    name = fields.Char(string='Name', required=True)
    class_ids = fields.One2many('education.class', 'school_id', string='Classes')
    code = fields.Char(string='Code', default='New', readonly=True)
    address = fields.Char(string='Address')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code') == 'New':  
                vals['code'] = self.env['ir.sequence'].next_by_code('education.school')
        return super().create(vals_list)
