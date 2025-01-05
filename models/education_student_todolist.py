from odoo import api,fields, models, _
from odoo.exceptions import UserError, ValidationError




class EducationStudentTodolist(models.Model):
    _name = 'education.student.todolist'
    _description = 'Education Student Todolist'

    name = fields.Char(string='Name')
    completed= fields.Boolean()
    color = fields.Char()   

