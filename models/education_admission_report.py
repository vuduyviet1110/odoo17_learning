from odoo import fields, models, tools

class EducationAdmissionReport(models.Model):
    _name = 'education.admission.report'
    _description = 'Education Admission Report'
    _auto = False
    # Các trường trong view
    student_id = fields.Many2one('education.student', string='Student', required=True, ondelete='cascade')
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
    _constraints = [
        ('student_id', 'unique(student_id)', 'Each student can only have one admission report.')
    ]

    # def _query_education_admission_report(self):
    #     """
    #     Define the SQL query to create the view.
    #     """
    #     _query = """
    #     SELECT 
    #         ecs.id AS schedule_id,                      -- ID của bảng lịch học
    #         ecs.day_of_week AS day_of_week,            -- Thứ trong tuần
    #         ecs.start_time AS start_time,              -- Thời gian bắt đầu
    #         ecs.end_time AS end_time,                  -- Thời gian kết thúc
    #         es.name AS student_name,                   -- Tên học sinh
    #         ear.start_date AS admission_start_date,    -- Ngày bắt đầu nhập học
    #         ear.end_date AS admission_end_date,        -- Ngày kết thúc nhập học
    #         ear.school_year_id AS school_year_id,      -- Năm học
    #         ear.state AS admission_state               -- Trạng thái nhập học
    #     FROM 
    #         education_class_schedule ecs               -- Bảng lịch học
    #     LEFT JOIN 
    #         education_student es ON ecs.student_id = es.id  -- Liên kết với bảng học sinh
    #     LEFT JOIN 
    #         education_admission_report ear ON es.id = ear.student_id  -- Liên kết với bảng báo cáo nhập học
    #     WHERE 
    #         es.active = TRUE                             -- Chỉ lấy học sinh đang hoạt động

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
