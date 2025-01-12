from odoo import fields, models, api

class EducationClassSchedule(models.Model):
    _name = 'education.class.schedule'
    _description = 'Education Class Schedule'

    student_id = fields.Many2one('education.student', string='Student', required=True)
    class_group_id = fields.Many2one('education.class.group', string='Class Group', required=True)
    day_of_week = fields.Selection([('monday', 'Monday'), 
                                    ('tuesday', 'Tuesday'),
                                    ('wednesday', 'Wednesday'),
                                    ('thursday', 'Thursday'),
                                    ('friday', 'Friday'),
                                    ('saturday', 'Saturday'),
                                    ('sunday', 'Sunday')], 
                                   string='Day of Week', required=True)
    start_time = fields.Float(string='Start Time', required=True)  
    end_time = fields.Float(string='End Time', required=True) 
