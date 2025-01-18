from odoo import http
import json

class StudentController(http.Controller):
    @http.route('/student/details', type='http', auth='public')
    def student_details(self):
        student = {
            'name': 'John Doe',
            'school': 'High School 1',
            'class': '10A',
            'mobile': '123456789',
            'state': 'California',
        }
        return http.Response(
            json.dumps(student), 
            content_type='application/json; charset=utf-8'
        )
