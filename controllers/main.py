from odoo import http
from odoo.http import request

class EducationStudentController(http.Controller):
    @http.route('/students/form', auth='public', type='http', website=True)
    def student_form(self, **kwargs):
        student = request.env['education.student'].sudo().create({
            'name': 'Student controller test',
        })
        
        # Render view form
        return request.render('education.education_student_view_form', {
            'student': student
        })
