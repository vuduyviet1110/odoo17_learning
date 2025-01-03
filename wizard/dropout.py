from odoo import api, fields, models

class DropDownWizard(models.TransientModel):
    _name = "education.dropout.wizard"
    _description = "Cancel Appointment Wizard"

    _name = 'education.student.dropout.wizard'
    _description = 'Education Student Dropout Wizard'

    def _default_student(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        return self.env[active_model].browse(active_id)
    

    student_id = fields.Many2one('education.student', string='Student', default=_default_student, required=True)
    dropout_reason = fields.Text(string='Dropout Reason', required=True)


    def action_confirm_dropout(self):
        self.student_id.dropout_reason = self.dropout_reason
        self.student_id.state = 'off'
        return {'type': 'ir.actions.act_window_close'}