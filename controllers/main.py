from odoo import http
from odoo.http import request

class StudentController(http.Controller):

    @http.route('/student/form', type='http', auth="user", website=True)
    def student_form(self, **kwargs):
        student = request.env['education.student'].search([('id', '=', 1)], limit=1) 
        
        return request.render('v_education.action_student_form', {
            'student': student,
        })
