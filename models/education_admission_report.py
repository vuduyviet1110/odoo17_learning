from odoo import fields, models, tools

class EducationAdmissionReport(models.Model):
    _name = 'education.admission.report'
    _description = 'Education Admission Report'
    _auto = False

    # Các trường trong view
    name = fields.Char(string='Name', readonly=True)
    start_date = fields.Date(string='Start Date', readonly=True)
    end_date = fields.Date(string='End Date', readonly=True)
    school_year_id = fields.Many2one('education.school.year', string='School Year', readonly=True)
    state = fields.Selection([
        ('draft', 'New'),
        ('confirmed', 'Confirmed'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', readonly=True)
    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ], string='Day of Week', readonly=True)
    start_time = fields.Float(string='Start Time', readonly=True)
    end_time = fields.Float(string='End Time', readonly=True)

    # def _query_education_admission_report(self):
    #     """
    #     Định nghĩa truy vấn SQL để tạo view.
    #     """
    #     _query = """
    #         SELECT 
    #             scs.id AS id,  -- ID của bảng schedule để làm khóa chính
    #             scs.day_of_week AS day_of_week,
    #             scs.start_time AS start_time,
    #             scs.end_time AS end_time,
    #             std.name AS name,  -- Tên của student từ bảng education_student
    #             ear.start_date AS start_date,
    #             ear.end_date AS end_date,
    #             ear.school_year_id AS school_year_id,
    #             ear.state AS state
    #         FROM 
    #             education_class_schedule scs
    #         LEFT JOIN 
    #             education_student std ON scs.student_id = std.id
    #         LEFT JOIN 
    #             education_admission_report ear ON std.id = ear.student_id
    #         WHERE 
    #             std.active = True
    #     """
    #     return _query

    # def init(self):
    #     """
    #     Tạo hoặc thay thế view trong cơ sở dữ liệu.
    #     """
    #     tools.drop_view_if_exists(self.env.cr, self._table)
    #     self.env.cr.execute("""
    #         CREATE OR REPLACE VIEW %s AS (%s)
    #     """ % (self._table, self._query_education_admission_report()))
