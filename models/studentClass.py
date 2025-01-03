from odoo import fields, models

class EducationClass(models.Model):
   _name = 'education.class'
   _description = 'Education Class'

   name = fields.Char(string='Name', required=True)

   school_id = fields.Many2one('education.school', string='School')
   class_ids = fields.One2many('education.class', 'school_id', string='Classes')
   student_ids = fields.One2many('education.student', 'class_id', string='Students')
   teacher_ids = fields.Many2many('res.partner', string='Teachers')


   def get_all_students(self):
        student = self.env['education.student']
        all_students = student.search([])
        print("All Students: ", all_students)



  