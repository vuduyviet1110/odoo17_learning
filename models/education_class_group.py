from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class EducationClassGroup(models.Model):  
    _name = 'education.class.group'
    _description = 'Education Class Group'
    _parent_store = True
    _parent_name = "parent_id"

    parent_path = fields.Char(index=True)
    name = fields.Char(string='Name', translate=True, required=True)
    parent_id = fields.Many2one('education.class.group', string='Parent Group', ondelete='restrict')
    child_ids = fields.One2many('education.class.group', 'parent_id', string='Child Groups', ondelete='restrict')  # Chỉ định inverse_name

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive categories.'))
