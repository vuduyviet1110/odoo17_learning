from odoo import fields, models, tools

class EducationAdmissionReport(models.Model):
    _name = 'education.admission.report'
    _description = 'Education Admission Report'
    _auto = False
    # name = models.CharField(string='Name')
    student_id = fields.Many2one('education.student', string='Student', required=True)
    school_id = fields.Many2one('education.school', string='School', required=True)
    school_name = fields.Char(string='School', related='student_id.school_id.name', readonly=True)
    class_id = fields.Many2one('education.class', string='Class', required=True)
    class_name = fields.Char(string='Class', related='student_id.class_id.name', readonly=True)
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    state = fields.Selection(
        selection=[('new', 'New'), ('studying', 'Studying'), ('off', 'Off')],
        related='student_id.state', 
        string='State'
    )
    student_code = fields.Char(string='Student Code', related='student_id.student_code' )

    def init(self):
        # Drop the view if it exists
        tools.drop_view_if_exists(self.env.cr, self._table)
        
        # Create the view
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW education_admission_report AS (
                SELECT 
                    row_number() OVER () AS id,
                    s.id as student_id,
                    s.name as name,
                    s.date_of_birth as start_date,
                    s.write_date::date as end_date,
                    s.class_id,
                    s.school_id,
                    s.student_code,
                    s.state
                FROM education_student s
                WHERE s.active = true
            )
        """)