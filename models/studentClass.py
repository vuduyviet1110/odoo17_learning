from odoo import fields, models,api
from datetime import datetime, timedelta
class EducationClass(models.Model):
   _name = 'education.class'
   _description = 'Education Class'

   miterm_test= fields.Date(string='Miterm Test')
   final_test= fields.Date(string='final Test')

   name = fields.Char(string='Name', required=True)
   school_id = fields.Many2one('education.school', string='School')
   class_ids = fields.One2many('education.class', 'school_id', string='Classes')
   student_ids = fields.One2many('education.student', 'class_id', string='Students')
   teacher_ids = fields.Many2many('res.partner', string='Teachers')
   class_group_id = fields.Many2one('education.class.group', string='Class Group')
   def get_all_students(self):
        student = self.env['education.student']
        all_students = student.search([])
        print("All Students: ", all_students)

   @api.model
   def send_mail_reminder(self):
      tomorrow = datetime.today().date() + timedelta(days=1)
      exams = self.search([('miterm_test', '=', tomorrow)])

      for exam in exams:
        students = self.env['education.student'].search([('class_id', '=', exam.id)])
        for student in students:
            student.send_mail_template()  

      


  