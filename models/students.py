from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date

class EducationStudent(models.Model):
    _name = 'education.student'
    _description = 'Education Student'

    name = fields.Char(string='Name', required=True, translate=True)
    student_code = fields.Char(string='Student Code', required=True, default='New', help="Student ID is unique")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', inverse='_inverse_age', search='_search_age',
                         store=False, compute_sudo=True)
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Internal Notes')
    country_id = fields.Many2one('res.country', 'Country')
    state_id = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=', country_id)]")
    mobile = fields.Char('Mobile')
    email = fields.Char('Email')
    image_128 = fields.Image('Image')
    attached_file = fields.Binary('Attached File', groups='base.group_user')
    description = fields.Html(string='Description', sanitize=True, strip_style=False)
    total_score = fields.Float(string='Total Score', digits=(3, 2))  
    write_date = fields.Datetime(string='Last Updated on')
    amount_paid = fields.Monetary(string="Amount Paid", currency_field="currency_id")
    currency_id = fields.Many2one('res.currency', string="Currency")
    state = fields.Selection(string='Status', selection=[('new', 'New'),('studying', 'Studying'),('off', 'Off')], default='new')
    dropout_reason = fields.Text(string='Dropout Reason')

    # trường liên kết
    class_id =fields.Many2one('education.class',string="Class",  ondelete="restrict")
    school_id = fields.Many2one('education.school', string='School')
    school_name = fields.Many2one('school_id.name', string='School')
    school_code = fields.Char(related='school_id.code', string='School Code')
    school_address = fields.Char(related='school_id.address', string='School Address')
    class_group_id = fields.Many2one('education.class.group', string='Class Group')

    _sql_constraints = [
        ('student_code_unique', 'unique(student_code)', "The student code must be unique!"),
        ('check_total_score', 'CHECK(total_score >= 0)', "The Total Score must be greater than or equal to 0!")
    ]

    def send_mail_template(self):
        template = self.env.ref('v_education.student_email_template')
        for rec in self:
            if rec.email:
                template.send_mail(rec.id, force_send=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('student_code') == 'New':  
                vals['student_code'] = self.env['ir.sequence'].next_by_code('education.student')
        return super().create(vals_list)

    @api.model
    def is_allowed_state(self, current_state, new_state):
        allowed_states = [('new', 'studying'), ('studying', 'off'), ('off', 'studying'), ('new', 'off')]
        return (current_state, new_state) in allowed_states

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError('Date of Birth must be in the past')

    @api.depends('date_of_birth')
    def _compute_age(self):
        current_year = fields.Date.today().year
        for record in self:
            if record.date_of_birth:
                record.age = current_year - record.date_of_birth.year
            else:
                record.age = 0

    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            self.class_group_id = self.class_id.class_group_id

    def _inverse_age(self):
        for record in self:
            if record.age and record.date_of_birth:
                current_year = fields.Date.today().year
                dob_year = current_year - record.age
                dob_month = record.date_of_birth.month
                dob_day = record.date_of_birth.day
                record.date_of_birth = date(dob_year, dob_month, dob_day)

    def _search_age(self, operator, value):
        current_year = fields.Date.today().year
        target_year = current_year - value
        new_value = date(target_year, 1, 1)
        operator_map = {'>': '<', '>=': '<=', '<': '>', '<=': '>='}
        new_operator = operator_map.get(operator, operator)
        return [('date_of_birth', new_operator, new_value)]

    def change_student_state(self, state):
            for student in self:
                if student.is_allowed_state(student.state, state):
                    student.state = state
                else:
                     raise UserError(_("Changing student status from %s to %s is not allowed.") % (student.state, state))

    def change_to_new(self):
        self.change_student_state('new')

    def change_to_studying(self):
        self.change_student_state('studying')

    def change_to_off(self):
        self.change_student_state('off')

    def find_student(self):
        domain = ['|', ('name', 'ilike', 'John'), ('class_id.name', '=', '12A1')]
        students = self.search(domain)

    @api.model
    def classes_has_student(self, all_classes):
        def has_student(_class):
            return len(_class.student) > 5
        return all_classes.filtered(has_student)
    
    @api.model
    def get_student_names(self, classes):
        return classes.mapped('student_ids.name')
    
    @api.model
    def sort_students_by_dob(self, students):
        return students.sorted(key='date_of_birth')
    

    @api.model
    def group_by_class(self):
        group_result = self.read_group(
            [('state', '=', 'studying')], # domain
            ['class_id'], # field
            ['class_id'] # group by
            )
        return group_result