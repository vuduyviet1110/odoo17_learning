from odoo import http

class StudentController(http.Controller):
    @http.route('/student/details', type='http', auth='public', website=True)
    def student_details(self):
        student = {
            'name': 'John Doe',
            'school': 'High School 1',
            'class': '10A',
            'mobile': '123456789',
            'state': 'California',
        }
        return http.request.render('v_education.student_template', {'student': student})
