from odoo import fields, models, api

class StudentLevel(models.Model):
   _name = 'student.level'
   _description = 'Student Level'
   _order = 'sequence, name'
   _rec_name = 'code'

   code = fields.Char(string='Code', required=True)
   name = fields.Char(string='Name', translate=True, required=True)
   sequence = fields.Integer(string='Sequence', default=1)

   def name_get(self):
      return [(order.id, '%s %s' % (_('Lunch Order'), '#%d' % order.id)) for order in self]