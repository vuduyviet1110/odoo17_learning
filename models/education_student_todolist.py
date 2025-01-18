from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class EducationStudentTodolist(models.Model):
    _name = 'education.student.todolist'
    _description = 'Education Student Todolist'

    student_id =fields.Many2one('education.student', string='Student', required=True)
    name = fields.Char(string='Name', required=True)
    completed = fields.Boolean(string='Completed', default=False)
    color = fields.Char(string='Color', help='Color code for the task')
    description = fields.Text(string='Description', help='Detailed description of the task')
    category = fields.Selection(
        [('personal', 'Personal'), ('work', 'Work'), ('study', 'Study'),('shopping', 'Shopping')],
        string='Category',
        default='personal',
        help='Category of the task'
    )
    due_date = fields.Date(string='Due Date', help='Task due date')

    @api.model
    def create(self, vals):
        """
        Override the create method to add any specific validations
        or behaviors when creating a task.
        """
        if not vals.get('name'):
            raise ValidationError(_("Task name is required."))
        return super(EducationStudentTodolist, self).create(vals)

    @api.constrains('color')
    def _check_color_format(self):
        """
        Ensure the color field is a valid hexadecimal color code.
        """
        for record in self:
            if record.color and not record.color.startswith('#') and len(record.color) != 7:
                raise ValidationError(_("Color must be a valid hexadecimal color code (e.g., #FFFFFF)."))
