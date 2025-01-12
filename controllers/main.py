from odoo import http
from odoo.http import request

class EducationStudentController(http.Controller):
    @http.route('/students/form', auth='public', type='http')
    def student_form(self, **kwargs):
        students = request.env['education.student'].sudo().search([])

        return request.render('education.education_student_view_form', {
            'students': students
        })